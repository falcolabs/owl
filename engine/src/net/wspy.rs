//! Webservice implementation for monkeys in the 21th century.
use crate::{logging, Packet};
use axum::{
    extract::{
        ws::{Message, WebSocket, WebSocketUpgrade},
        ConnectInfo,
    },
    http::StatusCode,
    response::{Html, IntoResponse},
    routing::get,
    Router,
};
use axum_extra::{headers, TypedHeader};
use futures::{stream::StreamExt, SinkExt};
use pyo3::prelude::*;
use std::{net::SocketAddr, path::PathBuf, sync::Arc};
use tokio::fs;
use tokio::sync::Mutex;
use tower::ServiceExt;
use tower_http::services::ServeDir;

pub type MessageHandler = std::sync::mpsc::Sender<RawRequest>;
/// Starts the web service. **This function contains
/// an intentional memory leak.**
///
/// # Arguments
/// * `on_message` - a closure or function pointer acting as
///                  the MessageHandler when a message comes in.
///                  Uses `Box<MessageHandler>` with the sole
///                  purpose to leak it.
///
/// # Examples
/// ```
/// start_webservice(Box::new(|_, _, _, _| {
///     Box::pin(async move {
///         something_async().await
///     })
/// }))
/// ```
#[tokio::main]
pub async fn start_webservice(
    call_mpsc: MessageHandler,
    listen_on: String,
    serve_dir: String,
    static_dir: String,
) {
    sws(call_mpsc, listen_on, serve_dir, static_dir).await;
}

async fn sws(call_mpsc: MessageHandler, listen_on: String, serve_dir: String, static_dir: String) {
    logging::info("Starting webserver initialization...");
    let app = Router::new()
        .fallback_service(get(|req| async move {
            let res = ServeDir::new(serve_dir).oneshot(req).await.unwrap();
            let status = res.status();
            match status {
                StatusCode::NOT_FOUND => {
                    let index_path = PathBuf::from(static_dir).join("404.html");
                    fs::read_to_string(index_path)
                        .await
                        .map(|index_content| (StatusCode::OK, Html(index_content)).into_response())
                        .unwrap_or_else(|_| {
                            (StatusCode::INTERNAL_SERVER_ERROR, "index.html not found")
                                .into_response()
                        })
                }
                _ => res.into_response(),
            }
        }))
        .route(
            "/harlem",
            get(move |ws, option, connect_info| ws_handler(ws, option, connect_info, call_mpsc)),
        );

    let listener = tokio::net::TcpListener::bind(listen_on).await.unwrap();
    logging::info("Serving on localhost:6942...");
    axum::serve(
        listener,
        app.into_make_service_with_connect_info::<SocketAddr>(),
    )
    .await
    .unwrap();
}

async fn ws_handler(
    ws: WebSocketUpgrade,
    _: Option<TypedHeader<headers::UserAgent>>,
    ConnectInfo(addr): ConnectInfo<SocketAddr>,
    call_hook: MessageHandler,
) -> impl IntoResponse {
    ws.on_upgrade(move |socket| handle_socket(socket, addr, call_hook))
}

#[pyclass]
#[derive(Clone)]
pub struct RawRequest {
    #[pyo3(get)]
    pub handle: IOHandle,
    #[pyo3(get)]
    pub sender: String,
    #[pyo3(get)]
    pub content: Packet,
}

#[pyclass]
#[derive(Clone, Debug)]
#[allow(dead_code)]
pub struct IOHandle {
    sender: Arc<Mutex<futures::stream::SplitSink<WebSocket, axum::extract::ws::Message>>>,
    receiver: Arc<Mutex<futures::stream::SplitStream<WebSocket>>>,
    addr: String,
}

impl PartialEq for IOHandle {
    fn eq(&self, other: &Self) -> bool {
        self.addr == other.addr
    }
}

impl Eq for IOHandle {}

#[pymethods]
impl IOHandle {
    pub async fn send(&mut self, msg: String) -> PyResult<()> {
        match self.sender.lock().await.send(Message::Text(msg)).await {
            Ok(_) => Ok(()),
            Err(e) => Err(pyo3::exceptions::PyConnectionResetError::new_err(format!(
                "Unable to send to handle {}: {}",
                self.addr, e
            ))),
        }
    }

    #[getter]
    pub fn addr(&self) -> String {
        self.addr.clone()
    }
}

/// Actual websocket statemachine (one will be spawned per connection)
async fn handle_socket(socket: WebSocket, who: SocketAddr, call_hook: MessageHandler) {
    logging::info(format!("{} connected.", who));

    let (s, r) = socket.split();
    let sender = Arc::new(Mutex::new(s));
    let receiver = Arc::new(Mutex::new(r));
    call_hook
        .send(RawRequest {
            handle: IOHandle {
                sender: Arc::clone(&sender),
                receiver: Arc::clone(&receiver),
                addr: who.to_string(),
            },
            sender: who.to_string(),
            content: Packet::Unknown {
                data: "CONNECTION INITIATED".to_string(),
            },
        })
        .unwrap();

    while let Some(Ok(msg)) = receiver.lock().await.next().await {
        let content = msg.to_text().expect("Error extracting text from Message");
        if call_hook
            .send(RawRequest {
                handle: IOHandle {
                    sender: Arc::clone(&sender),
                    receiver: Arc::clone(&receiver),
                    addr: who.to_string(),
                },
                sender: who.to_string(),
                content: serde_json::from_str(content).unwrap_or(Packet::Unknown {
                    data: content.to_string(),
                }),
            })
            .is_err()
        {
            logging::error("Failed to send RawRequest")
        }
        // let chbound = call_hook.bind(py);
        // logging::info("bound py.");
        // println!("{:#?}", chbound);
        // let coroutine = chbound
        //     .call1((
        //         IOHandle {
        //             sender: Arc::clone(&sender),
        //             receiver: Arc::clone(&receiver),
        //         },
        //         who.to_string(),
        //         msg.to_text().unwrap(),
        //     ))
        //     .expect("Unable to form coroutine.");
        // tokio::spawn();
    }

    call_hook
        .send(RawRequest {
            handle: IOHandle {
                sender: Arc::clone(&sender),
                receiver: Arc::clone(&receiver),
                addr: who.to_string(),
            },
            sender: who.to_string(),
            content: Packet::Unknown {
                data: "CONNECTION HALTED".to_string(),
            },
        })
        .unwrap();
}

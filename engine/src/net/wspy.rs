//! Webservice implementation for monkeys in the 21th century.
use crate::{logging, Packet};
use axum::{
    extract::ws::{Message, WebSocket},
    http::StatusCode,
    response::{Html, IntoResponse},
    routing::get,
    Router,
};
use futures::SinkExt;
use pyo3::prelude::*;
use std::{net::SocketAddr, path::PathBuf, sync::Arc};
use tokio::fs;
use tokio::sync::Mutex;
use tower::util::ServiceExt;
use tower_http::services::ServeDir;

use crate::net::{wsmain, wstime};

pub type MessageHandler = std::sync::mpsc::Sender<Notifier>;
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
    call_mpsc_main: MessageHandler,
    call_mpsc_time: MessageHandler,
    listen_on: String,
    serve_dir: String,
    static_dir: String,
) {
    sws(
        call_mpsc_main,
        call_mpsc_time,
        listen_on,
        serve_dir,
        static_dir,
    )
    .await;
}

async fn sws(
    call_mpsc_main: MessageHandler,
    call_mpsc_time: MessageHandler,
    listen_on: String,
    serve_dir: String,
    static_dir: String,
) {
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
            get(move |ws, option, connect_info| {
                wsmain::ws_handler(ws, option, connect_info, call_mpsc_main)
            }),
        )
        .route(
            "/time",
            get(move |ws, option, connect_info| {
                wstime::ws_handler(ws, option, connect_info, call_mpsc_time)
            }),
        );

    let listener = tokio::net::TcpListener::bind(listen_on.clone())
        .await
        .unwrap_or_else(|e| {
            panic!(
        "Bad host address. Make sure you provided a valid address (HOST:PORT) (you provided {:#?}): {}",
        listen_on, e
    )
        });
    logging::info(format!("Serving on {}...", listen_on));
    axum::serve(
        listener,
        app.into_make_service_with_connect_info::<SocketAddr>(),
    )
    .await
    .unwrap();
}

pub enum Notifier {
    RawRequest(RawRequest),
    ExecuteTick,
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

impl IOHandle {
    pub fn new(
        sender: Arc<Mutex<futures::stream::SplitSink<WebSocket, axum::extract::ws::Message>>>,
        receiver: Arc<Mutex<futures::stream::SplitStream<WebSocket>>>,
        addr: String,
    ) -> IOHandle {
        IOHandle {
            sender,
            receiver,
            addr,
        }
    }
}

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

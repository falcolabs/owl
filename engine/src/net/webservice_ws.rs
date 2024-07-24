//! Webservice implementation for monkeys in the 21th century.
use crate::logging;
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
use futures::{
    future::BoxFuture,
    stream::{SplitSink, SplitStream, StreamExt},
};
use std::{net::SocketAddr, path::PathBuf, sync::Arc};
use tokio::sync::Mutex;
use tokio::{fs, runtime::Builder};
use tower::ServiceExt;
use tower_http::services::ServeDir;

// 2 FUCKING DAYS
// FUCK ASYNC RUST (AND HIS MOTHER)
pub type MessageHandler = dyn Fn(
        Arc<Mutex<SplitSink<WebSocket, Message>>>,
        Arc<Mutex<SplitStream<WebSocket>>>,
        SocketAddr,
        Message,
    ) -> BoxFuture<'static, ()>
    + Send
    + Sync;

pub type Callback = Arc<Mutex<&'static mut MessageHandler>>;

/// Starts the web service. **This function contains
/// an intentional memory leak.**
///
/// # Arguments
/// * `on_message` - a closure or function pointer acting as
///                  the callback when a message comes in.
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
pub fn start_webservice(
    on_message: Box<MessageHandler>,
    listen_on: String,
    serve_dir: String,
    static_dir: String,
) {
    let runtime = Builder::new_multi_thread().enable_all().build().unwrap();
    // TODO - #1 intentional memory leak
    let radioactive_leak = Box::leak(on_message);
    runtime.block_on(sws(
        Arc::new(Mutex::new(radioactive_leak)),
        listen_on,
        serve_dir,
        static_dir,
    ));
}

async fn sws(call_hook: Callback, listen_on: String, serve_dir: String, static_dir: String) {
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
            get(move |ws, option, connect_info| ws_handler(ws, option, connect_info, call_hook)),
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
    call_hook: Callback,
) -> impl IntoResponse {
    ws.on_upgrade(move |socket| handle_socket(socket, addr, call_hook))
}

/// Actual websocket statemachine (one will be spawned per connection)
async fn handle_socket(socket: WebSocket, who: SocketAddr, call_hook: Callback) {
    logging::info(format!("{} connected.", who));

    tokio::spawn({
        let (s, r) = socket.split();
        let ch: Callback = Arc::clone(&call_hook);
        let sender = Arc::new(Mutex::new(s));
        let receiver = Arc::new(Mutex::new(r));
        async move {
            while let Some(Ok(msg)) = receiver.lock().await.next().await {
                logging::info(format!("From {}: {:#?}", who, msg));
                let mut cb = ch.lock().await;
                let n = cb(
                    // Arc::clone(&Arc::new(&mut sender)),
                    // Arc::clone(&Arc::new(&mut receiver)),
                    Arc::clone(&sender),
                    Arc::clone(&receiver),
                    who,
                    msg.clone(),
                );
                n.await;
            }
        }
    });
}

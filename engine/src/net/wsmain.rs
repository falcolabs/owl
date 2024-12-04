use crate::{logging, Packet};
use axum::{
    extract::{
        ws::{WebSocket, WebSocketUpgrade},
        ConnectInfo,
    },
    response::IntoResponse,
};
use axum_extra::{headers, TypedHeader};
use futures::stream::StreamExt;
use std::{net::SocketAddr, sync::Arc};
use tokio::sync::Mutex;

use super::wspy::{IOHandle, MessageHandler, Notifier, RawRequest};

pub async fn ws_handler(
    ws: WebSocketUpgrade,
    _: Option<TypedHeader<headers::UserAgent>>,
    ConnectInfo(addr): ConnectInfo<SocketAddr>,
    call_hook: MessageHandler,
) -> impl IntoResponse {
    ws.on_upgrade(move |socket| handle_socket(socket, addr, call_hook))
}

/// Actual websocket statemachine (one will be spawned per connection)
async fn handle_socket(socket: WebSocket, who: SocketAddr, call_hook: MessageHandler) {
    logging::info(format!("{} connected.", who));

    let (s, r) = socket.split();
    let sender = Arc::new(Mutex::new(s));
    let receiver = Arc::new(Mutex::new(r));
    call_hook
        .send(Notifier::RawRequest(RawRequest {
            handle: IOHandle::new(Arc::clone(&sender), Arc::clone(&receiver), who.to_string()),
            sender: who.to_string(),
            content: Packet::Unknown {
                data: "CONNECTION INITIATED".to_string(),
            },
        }))
        .unwrap();

    while let Some(Ok(msg)) = receiver.lock().await.next().await {
        let content = msg.to_text().expect("Error extracting text from Message");
        if call_hook
            .send(Notifier::RawRequest(RawRequest {
                handle: IOHandle::new(Arc::clone(&sender), Arc::clone(&receiver), who.to_string()),
                sender: who.to_string(),
                content: serde_json::from_str(content).unwrap_or(Packet::Unknown {
                    data: content.to_string(),
                }),
            }))
            .is_err()
        {
            logging::error("Failed to send RawRequest")
        }
    }

    call_hook
        .send(Notifier::RawRequest(RawRequest {
            handle: IOHandle::new(Arc::clone(&sender), Arc::clone(&receiver), who.to_string()),
            sender: who.to_string(),
            content: Packet::Unknown {
                data: "CONNECTION HALTED".to_string(),
            },
        }))
        .unwrap();
}

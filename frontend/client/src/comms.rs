use crate::console_log;
use engine::Packet;
use std::sync::Arc;
use wasm_bindgen::prelude::*;
pub use web_sys::{ErrorEvent, MessageEvent, WebSocket};

#[derive(Debug, Clone)]
#[wasm_bindgen]
#[allow(unused)]
pub struct Message {
    ws: Arc<WebSocket>,
    content: Packet,
}

impl Message {
    pub fn new(ws: Arc<WebSocket>, content: Packet) -> Message {
        Message { ws, content }
    }

    pub fn ws(&self) -> Arc<WebSocket> {
        Arc::clone(&self.ws)
    }

    pub fn content(&self) -> Packet {
        self.content.clone()
    }
}

pub fn start_ws() -> Arc<WebSocket> {
    let ws = Arc::new(WebSocket::new("ws://localhost:6942/harlem").expect("what the fuck"));
    ws.set_binary_type(web_sys::BinaryType::Arraybuffer);

    let oec = Closure::<dyn FnMut(_)>::new(move |e: ErrorEvent| {
        console_log!("error event: {:?}", e);
    });
    ws.set_onerror(Some(oec.as_ref().unchecked_ref()));
    oec.forget();

    let onopen_callback = Closure::<dyn FnMut()>::new(move || {
        console_log!("Socket opened.");
    });
    ws.set_onopen(Some(onopen_callback.as_ref().unchecked_ref()));
    onopen_callback.forget();

    ws
}

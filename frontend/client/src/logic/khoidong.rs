use super::MessageHandler;
use crate::comms;
use async_trait::async_trait;
use engine::Packet;
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
#[derive(Debug)]
pub struct KhoiDong {}

#[wasm_bindgen]
impl KhoiDong {
    #[wasm_bindgen(constructor)]
    pub fn constructor() -> KhoiDong {
        KhoiDong {}
    }
}

#[async_trait(?Send)]
impl MessageHandler for KhoiDong {
    async fn on_message(&mut self, _ctx: &mut comms::WsHandle, _msg: Packet) {}
}

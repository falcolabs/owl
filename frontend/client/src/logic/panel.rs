use super::MessageHandler;
use crate::{
    comms::{self, ClientPacket},
    console_log,
};
use async_trait::async_trait;
use engine::Packet;
use wasm_bindgen::prelude::*;

#[wasm_bindgen(skip_typescript, inspectable)]
#[derive(Debug)]
pub struct Panel {}

#[wasm_bindgen]
impl Panel {
    #[wasm_bindgen(constructor)]
    pub fn constructor() -> Panel {
        Panel {}
    }

    pub fn inspect(t: &JsValue) {
        console_log!("inspect result: {:#?}", t);
    }

    pub fn cpacket_test(cp: ClientPacket) {
        let p: Packet = cp.into();
        console_log!("packet: {:#?}", p);
    }
}

#[async_trait(?Send)]
impl MessageHandler for Panel {
    async fn on_message(&mut self, _ctx: &mut comms::WsHandle, _msg: Packet) {}
}

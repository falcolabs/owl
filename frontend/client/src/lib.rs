pub use objutils::*;

use core::panic;
use wasm_bindgen::prelude::*;

pub mod bridge;
pub mod objutils;
pub mod tstypes;

use bridge::ClientPacket;

#[wasm_bindgen(skip_typescript)]
#[allow(unused)]
pub struct ClientHandle {
    send_hook: js_sys::Function,
}

#[wasm_bindgen]
#[allow(unused)]
impl ClientHandle {
    #[wasm_bindgen(constructor)]
    pub fn new() -> ClientHandle {
        panic!("no dont use this bruh use .create()");
    }

    pub fn wrap(send_hook: js_sys::Function) -> ClientHandle {
        Self { send_hook }
    }

    pub fn parse(message: String) -> ClientPacket {
        ClientPacket::from(serde_json::from_str::<engine::Packet>(&message).unwrap())
    }

    pub async fn send(&mut self, packet: ClientPacket) -> Result<(), JsValue> {
        self.send_hook.call1(&JsValue::null(), &packet.into())?;
        Ok(())
    }

    /// Fishes out panics.
    pub fn set_panic_hook() {
        bridge::set_panic_hook();
    }
}

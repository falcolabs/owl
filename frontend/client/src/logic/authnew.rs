use async_trait::async_trait;
use engine::prelude::*;
use engine::Packet;
use js_sys::Object;
use wasm_bindgen::prelude::*;

use crate::comms;
use crate::console_log;
use crate::property_getter;

use super::MessageHandler;
#[wasm_bindgen]
#[derive(Debug)]
pub struct Auth {
    on_success: js_sys::Function,
}

#[wasm_bindgen]
impl Auth {
    #[wasm_bindgen(constructor)]
    pub fn constructor(on_success: js_sys::Function) -> Auth {
        Auth { on_success }
    }

    pub fn new(obj: &Object) -> Auth {
        Auth {
            on_success: crate::extractjs(obj, "on_success"),
        }
    }

    pub async fn login(&self, handle: &mut comms::WsHandle, username: String, access_key: String) {
        handle
            .send(Packet::CommenceSession {
                data: Credentials {
                    username,
                    access_key,
                },
            })
            .await
            .unwrap();
    }
}

property_getter!(Auth, on_success, js_sys::Function);

#[async_trait(?Send)]
impl MessageHandler for Auth {
    async fn on_message(&mut self, _ctx: &mut comms::WsHandle, msg: Packet) {
        console_log!("got a message");
        if let Packet::AuthStatus { data: authstatus } = msg {
            if authstatus.success {
                let _ = self.on_success.call1(&JsValue::null(), &JsValue::TRUE);
            } else {
                let _ = self.on_success.call1(&JsValue::null(), &JsValue::FALSE);
            }
        }
    }
}

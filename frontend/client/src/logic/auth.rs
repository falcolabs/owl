use crate::{comms::Message, Context};
use engine::{Credentials, Packet};
use js_sys::Object;
use wasm_bindgen::prelude::*;
#[wasm_bindgen]
pub struct Auth {
    obj: js_sys::Object,
}

#[wasm_bindgen]
#[allow(unused)]
impl Auth {
    #[wasm_bindgen(constructor)]
    pub fn constructor(on_success: js_sys::Function) -> Auth {
        let obj = Object::new();
        let login = Closure::wrap(Box::new(move || {}) as Box<dyn Fn() -> ()>);
        Object::define_property(
            &obj,
            &JsValue::from_str("login"),
            &login.as_ref().clone().dyn_into().unwrap(),
        );
        Object::define_property(&obj, &JsValue::from_str("on_success"), &on_success);

        Auth { obj }
    }

    pub fn on_success(&self) -> js_sys::Function {
        Object::get_own_property_descriptor(&self.obj, &JsValue::from_str("on_success"))
            .dyn_into()
            .unwrap()
    }

    pub fn login(&self, c: Context, username: String, access_key: String) {
        c.ws.send_with_str(
            Packet::CommenceSession {
                data: Credentials {
                    username,
                    access_key,
                },
            }
            .to_string()
            .as_str(),
        )
        .unwrap();
    }

    pub fn on_message(data: js_sys::Object, msg: Message) {
        let instance = Auth { obj: data };
        if let Packet::AuthStatus { data: authstatus } = msg.content() {
            if authstatus.success {
                instance
                    .on_success()
                    .call1(&JsValue::null(), &JsValue::TRUE);
            } else {
                instance
                    .on_success()
                    .call1(&JsValue::null(), &JsValue::FALSE);
            }
        }
    }
}

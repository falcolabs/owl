use js_sys::JsString;
pub use logic::*;

use comms::Message;
use engine::Packet;

use std::str::FromStr;
use std::sync::Arc;
use std::sync::Mutex;
use wasm_bindgen::prelude::*;
use web_sys::MessageEvent;

pub mod comms;
pub mod jsbridge;
pub mod logic;

#[wasm_bindgen]
#[allow(unused)]
pub struct Context {
    part_name: &'static str,
    ws: Arc<comms::WebSocket>,
    handler: Arc<Box<dyn Fn(js_sys::Object, Message)>>,
}

#[wasm_bindgen]
#[allow(unused)]
impl Context {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Context {
        panic!("no dont use this bruh use .create()");
    }

    pub async fn create(init_logic: js_sys::Function) -> Context {
        let ws = comms::start_ws();
        let obj = init_logic
            .call1(
                &JsValue::null(),
                &JsString::from_str("auth").expect("Converting to JsString failed."),
            )
            .expect("Executing init_logic failed.")
            .dyn_into::<js_sys::Object>()
            .expect("Casting init_logic result into object failed.");

        while ws.ready_state() != 1 {
            console_log!("WebSocket is not ready, retrying in 100ms...");
            jsbridge::sleep(100).await;
        }

        ws.send_with_str(
            Packet::RequestResource {
                data: engine::ResourceRequest::CurrentPart {},
            }
            .to_string()
            .as_str(),
        )
        .expect("You have excellent internet, we failed in sending Packet::RequestResource");
        let wsclone1 = Arc::clone(&ws);
        let mut ret = Arc::new(Mutex::new(Context {
            part_name: "",
            ws: Arc::clone(&ws),
            handler: Arc::new(Box::new(|_, _| {})),
        }));
        let mut rclone1 = Arc::clone(&ret);
        let objc = obj.clone();
        let ocb = Closure::<dyn FnMut(MessageEvent)>::new(move |msg: MessageEvent| {
            let packet: Packet =
                serde_wasm_bindgen::from_value(msg.data()).expect("Deserialization failed.");
            if let Packet::Part { data: cp } = packet {
                match cp.name.as_str() {
                    "auth" => {
                        drop(cp);
                        rclone1
                            .lock()
                            .expect("Locking rclone1 failed part_name")
                            .part_name = "auth";
                        rclone1
                            .lock()
                            .expect("Locking rclone1 failed handler")
                            .handler = Arc::new(Box::new(logic::auth::Auth::on_message));
                        // Option::Some(Arc::new(Mutex::new(logic::auth::Auth { obj })));
                    }
                    _ => {}
                }
            }
        });
        ws.set_onmessage(Some(ocb.as_ref().unchecked_ref()));
        drop(ocb);
        let wsclone2 = Arc::clone(&ws);
        ret.clear_poison();
        let objc2 = obj.clone();
        let rclone2 = Arc::clone(&ret);
        let ocb = Closure::<dyn FnMut(MessageEvent)>::new(move |msg: MessageEvent| {
            let packet: Packet = serde_wasm_bindgen::from_value(js_sys::JSON::parse(
                &msg.data().as_string().unwrap(),
            ).expect("Deserializing Packet failed."))
            .expect("Destructuring packet to Rust struct failed.");
            (rclone2.lock().expect("Locking rclone2 failed.").handler)(
                objc2.clone(),
                Message::new(Arc::clone(&wsclone2), packet),
            );
        });
        ws.set_onmessage(Some(ocb.as_ref().unchecked_ref()));
        ocb.forget();
        let retlocked2 = Arc::clone(&ret);
        let r2 = retlocked2.lock().expect("Locking retlocked2 failed.");
        Context {
            part_name: r2.part_name,
            ws: r2.ws.clone(),
            handler: Arc::clone(&r2.handler),
        }
    }

    pub fn part_name(&self) -> String {
        String::from(self.part_name)
    }
}

/// This trap baits panics and help you
/// fish out pesky errors which otherwise prints
/// gibberish hex address code in the browser console.
#[wasm_bindgen]
pub fn panic_bait() {
    jsbridge::set_panic_hook();
    console_log!("Panic hook has been set. WebAssembly module has finished loading.");
}

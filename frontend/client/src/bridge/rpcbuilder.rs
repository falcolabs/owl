use engine::{self, universal::PortableValue};
use js_sys::JSON;
use wasm_bindgen::prelude::*;
pub use web_sys::{ErrorEvent, MessageEvent, WebSocket};

#[wasm_bindgen]
pub struct RPCBuilder {
    call: engine::ProcedureCall,
}

#[wasm_bindgen]
impl RPCBuilder {
    #[wasm_bindgen(constructor)]
    pub fn new(name: &str) -> RPCBuilder {
        RPCBuilder {
            call: engine::ProcedureCall::new(name),
        }
    }

    pub fn param(
        mut self,
        name: &str,
        v: &JsValue,
        type_annotation: engine::universal::PortableType,
    ) -> RPCBuilder {
        self.call.append_arg(
            name,
            PortableValue::new(
                JSON::stringify(v)
                    .expect("Unable to serialize procedure parameter")
                    .as_string()
                    .unwrap()
                    .as_str(),
                type_annotation,
            ),
        );
        self
    }

    pub async fn build(self) -> crate::bridge::ClientPacket {
        crate::bridge::ClientPacket::from(engine::Packet::CallProcedure { data: self.call })
    }
}

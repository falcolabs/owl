use wasm_bindgen::prelude::*;

#[wasm_bindgen(typescript_custom_section)]
const TS_APPEND_CONTENT: &'static str = concat!(
    include_str!("../types/client.d.ts"),
    include_str!("../types/logic/panel.d.ts")
);

use crate::bridge::{ClientPacket, QueryPacket, QueryType};
use wasm_bindgen::prelude::*;

#[wasm_bindgen(inspectable, skip_typescript)]
pub struct Query {}

#[wasm_bindgen]
impl Query {
    #[wasm_bindgen(js_name = player)]
    pub fn player(value: JsValue) -> ClientPacket {
        QueryPacket::new(QueryType::Player, value).into()
    }
    #[wasm_bindgen(js_name = question)]
    pub fn question(value: JsValue) -> ClientPacket {
        QueryPacket::new(QueryType::Question, value).into()
    }
    #[wasm_bindgen(js_name = partById)]
    pub fn part_by_id(value: JsValue) -> ClientPacket {
        QueryPacket::new(QueryType::PartByID, value).into()
    }
    #[wasm_bindgen(js_name = partByName)]
    pub fn part_by_name(value: JsValue) -> ClientPacket {
        QueryPacket::new(QueryType::PartByName, value).into()
    }
    #[wasm_bindgen(js_name = state)]
    pub fn state(value: JsValue) -> ClientPacket {
        QueryPacket::new(QueryType::State, value).into()
    }
    #[wasm_bindgen(js_name = playerList)]
    pub fn player_list(value: JsValue) -> ClientPacket {
        QueryPacket::new(QueryType::PlayerList, value).into()
    }
    #[wasm_bindgen(js_name = questionBank)]
    pub fn question_bank() -> ClientPacket {
        QueryPacket::new(QueryType::QuestionBank, JsValue::null()).into()
    }
    #[wasm_bindgen(js_name = show)]
    pub fn show() -> ClientPacket {
        QueryPacket::new(QueryType::Show, JsValue::null()).into()
    }
    #[wasm_bindgen(js_name = ticker)]
    pub fn ticker() -> ClientPacket {
        QueryPacket::new(QueryType::Ticker, JsValue::null()).into()
    }
    #[wasm_bindgen(js_name = timer)]
    pub fn timer() -> ClientPacket {
        QueryPacket::new(QueryType::Timer, JsValue::null()).into()
    }
    #[wasm_bindgen(js_name = currentPart)]
    pub fn current_part() -> ClientPacket {
        QueryPacket::new(QueryType::CurrentPart, JsValue::null()).into()
    }
    #[wasm_bindgen(js_name = availableProcedures)]
    pub fn available_procedures() -> ClientPacket {
        QueryPacket::new(QueryType::AvailableProcedures, JsValue::null()).into()
    }
    #[wasm_bindgen(js_name = stateList)]
    pub fn state_list() -> ClientPacket {
        QueryPacket::new(QueryType::StateList, JsValue::null()).into()
    }
}

use core::fmt;

use gloo_utils::format::JsValueSerdeExt;
use js_sys::{JsString, Object, Reflect};
use serde::{Deserialize, Serialize};
use wasm_bindgen::prelude::*;

#[wasm_bindgen(skip_typescript)]
#[derive(Serialize, Deserialize, Clone, Copy, PartialEq, Eq, Debug)]
pub enum QueryType {
    Player = 0,
    Question = 1,
    PartByID = 2,
    PartByName = 3,
    QuestionBank = 4,
    Show = 5,
    Ticker = 6,
    Timer = 7,
    CurrentPart = 8,
    AvailableProcedures = 9,
    GameState = 10,
}

impl Into<f64> for QueryType {
    fn into(self) -> f64 {
        (self as u8) as f64
    }
}

impl fmt::Display for QueryType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

#[wasm_bindgen(skip_typescript)]
#[derive(Debug, Clone)]
pub struct QueryPacket {
    pub variant: QueryType,
    index: JsValue,
}

impl From<Object> for QueryPacket {
    fn from(value: Object) -> QueryPacket {
        QueryPacket::new(
            match Reflect::get(&value, &JsString::from("variant").into())
                .unwrap()
                .as_f64()
                .unwrap()
            {
                0.0 => QueryType::Player,
                1.0 => QueryType::Question,
                2.0 => QueryType::PartByID,
                3.0 => QueryType::PartByName,
                4.0 => QueryType::QuestionBank,
                5.0 => QueryType::Show,
                6.0 => QueryType::Ticker,
                7.0 => QueryType::Timer,
                8.0 => QueryType::CurrentPart,
                9.0 => QueryType::AvailableProcedures,
                10.0 => QueryType::GameState,
                _ => panic!("Unknown QueryType"),
            },
            match Reflect::get(&value, &JsValue::from("index")) {
                Ok(index) => index.into(),
                Err(_) => JsValue::null().into(),
            },
        )
    }
}

impl Into<Object> for QueryPacket {
    fn into(self) -> Object {
        let obj = Object::new();
        Reflect::set(
            &obj,
            &JsValue::from("variant"),
            &JsValue::from_f64(self.variant.into()),
        )
        .unwrap();
        Reflect::set(&obj, &JsValue::from("index"), &self.index).unwrap();
        obj
    }
}

impl Into<crate::bridge::ClientPacket> for QueryPacket {
    fn into(self) -> crate::bridge::ClientPacket {
        crate::bridge::ClientPacket::new(crate::bridge::PacketType::Query, self.into())
    }
}

#[wasm_bindgen]
impl QueryPacket {
    #[wasm_bindgen(constructor)]
    pub fn new(variant: QueryType, index: JsValue) -> Self {
        Self { variant, index }
    }
}

macro_rules! requestentry {
    ($self:ident->$variant:ident) => {
        engine::Packet::Query {
            data: engine::Query::$variant {
                index: $self.index.into_serde().unwrap(),
            },
        }
    };
    ($variant:ident) => {
        engine::Packet::Query {
            data: engine::Query::$variant {},
        }
    };
}

impl Into<engine::Packet> for QueryPacket {
    fn into(self) -> engine::Packet {
        match self.variant {
            QueryType::Player => requestentry!(self->Player),
            QueryType::Question => requestentry!(self->Question),
            QueryType::PartByID => requestentry!(self->PartByID),
            QueryType::PartByName => requestentry!(self->PartByName),
            QueryType::QuestionBank => requestentry!(QuestionBank),
            QueryType::Show => requestentry!(Show),
            QueryType::Ticker => requestentry!(Ticker),
            QueryType::Timer => requestentry!(Timer),
            QueryType::CurrentPart => requestentry!(CurrentPart),
            QueryType::AvailableProcedures => requestentry!(AvailableProcedures),
            QueryType::GameState => requestentry!(GameState),
        }
    }
}

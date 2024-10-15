use core::fmt;

use gloo_utils::format::JsValueSerdeExt;
use js_sys::{JsString, Object, Reflect};
use serde_repr::{Deserialize_repr, Serialize_repr};
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
#[derive(Serialize_repr, Deserialize_repr, Clone, Copy, PartialEq, Eq, Debug)]
#[repr(u8)]
pub enum QueryType {
    Player = 0,
    Question = 1,
    PartByID = 2,
    PartByName = 3,
    State = 4,
    PlayerList = 5,
    QuestionBank = 6,
    Ticker = 7,
    Timer = 8,
    CurrentPart = 9,
    AvailableProcedures = 10,
    StateList = 11,
    PartList = 12,
    Log = 13,
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
                4.0 => QueryType::State,
                5.0 => QueryType::PlayerList,
                6.0 => QueryType::QuestionBank,
                7.0 => QueryType::Ticker,
                8.0 => QueryType::Timer,
                9.0 => QueryType::CurrentPart,
                10.0 => QueryType::AvailableProcedures,
                11.0 => QueryType::StateList,
                12.0 => QueryType::PartList,
                13.0 => QueryType::Log,
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
            QueryType::State => requestentry!(self->State),
            QueryType::PlayerList => requestentry!(PlayerList),
            QueryType::QuestionBank => requestentry!(QuestionBank),
            QueryType::Ticker => requestentry!(Ticker),
            QueryType::Timer => requestentry!(Timer),
            QueryType::CurrentPart => requestentry!(CurrentPart),
            QueryType::AvailableProcedures => requestentry!(AvailableProcedures),
            QueryType::StateList => requestentry!(StateList),
            QueryType::PartList => requestentry!(PartList),
            QueryType::Log => requestentry!(self->Log),
        }
    }
}

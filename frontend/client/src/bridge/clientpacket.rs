use core::fmt;

use gloo_utils::format::JsValueSerdeExt;
use js_sys::{Object, Reflect};
use serde::{Deserialize, Serialize};
use wasm_bindgen::prelude::*;

use crate::console_log;

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
#[wasm_bindgen(skip_typescript)]
#[allow(unused)]
pub enum PacketType {
    Player = 0,
    Part = 1,
    Question = 2,
    QuestionBank = 3,
    Show = 4,
    Ticker = 5,
    Timer = 6,
    CommenceSession = 7,
    AuthStatus = 8,
    Query = 9,
    ProcedureList = 10,
    CallProcedure = 11,
    StateList = 12,
    State = 13,
    UpdateState = 14,
    Unknown = 15,
}

impl Into<f64> for PacketType {
    fn into(self) -> f64 {
        (self as u8) as f64
    }
}

impl fmt::Display for PacketType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

#[derive(Debug, Clone)]
#[wasm_bindgen(skip_typescript, inspectable, js_name = Packet)]
pub struct ClientPacket {
    pub variant: PacketType,
    value: js_sys::Object,
}

#[wasm_bindgen(js_class = Packet)]
impl ClientPacket {
    #[wasm_bindgen(constructor)]
    pub fn new(ptype: PacketType, value: Object) -> ClientPacket {
        ClientPacket {
            variant: ptype,
            value,
        }
    }

    #[wasm_bindgen(getter)]
    pub fn value(&self) -> JsValue {
        Reflect::get(
            &Reflect::get(&self.value, &JsValue::from_str(&self.variant.to_string())).unwrap(),
            &JsValue::from_str("data"),
        )
        .unwrap()
        .clone()
        .dyn_into()
        .unwrap()
    }

    pub fn pack(&self) -> String {
        // JsValue::into(self)
        <ClientPacket as Into<engine::Packet>>::into(self.clone().into()).pack()
    }
}

impl Into<Object> for ClientPacket {
    fn into(self) -> Object {
        let output = Object::new();
        Reflect::set(
            &output,
            &JsValue::from("variant"),
            &JsValue::from_f64(self.variant.into()),
        )
        .unwrap();
        Reflect::set(&output, &JsValue::from("value"), &self.value).unwrap();
        output
    }
}

macro_rules! packet_conv {
    ($self:ident->$variant:ident) => {
        engine::Packet::$variant {
            data: <Object as Into<JsValue>>::into($self.value)
                .into_serde()
                .unwrap(),
        }
    };
}

impl Into<engine::Packet> for ClientPacket {
    fn into(self) -> engine::Packet {
        match self.variant {
            PacketType::Player => packet_conv!(self->Player),
            PacketType::Part => packet_conv!(self->Part),
            PacketType::Question => packet_conv!(self->Question),
            PacketType::QuestionBank => packet_conv!(self->QuestionBank),
            PacketType::Show => packet_conv!(self->Show),
            PacketType::Ticker => packet_conv!(self->Ticker),
            PacketType::Timer => packet_conv!(self->Timer),
            PacketType::CommenceSession => packet_conv!(self->CommenceSession),
            PacketType::AuthStatus => packet_conv!(self->AuthStatus),
            PacketType::ProcedureList => packet_conv!(self->ProcedureList),
            PacketType::CallProcedure => packet_conv!(self->CallProcedure),
            PacketType::StateList => packet_conv!(self->StateList),
            PacketType::State => packet_conv!(self->State),
            PacketType::UpdateState => packet_conv!(self->UpdateState),
            PacketType::Unknown => packet_conv!(self->Unknown),
            PacketType::Query => crate::bridge::QueryPacket::from(self.value).into(),
        }
    }
}

impl From<engine::Packet> for ClientPacket {
    fn from(packet: engine::Packet) -> Self {
        let ptype = match packet {
            engine::Packet::Player { .. } => PacketType::Player,
            engine::Packet::Part { .. } => PacketType::Part,
            engine::Packet::Question { .. } => PacketType::Question,
            engine::Packet::QuestionBank { .. } => PacketType::QuestionBank,
            engine::Packet::Show { .. } => PacketType::Show,
            engine::Packet::Ticker { .. } => PacketType::Ticker,
            engine::Packet::Timer { .. } => PacketType::Timer,
            engine::Packet::CommenceSession { .. } => PacketType::CommenceSession,
            engine::Packet::AuthStatus { .. } => PacketType::AuthStatus,
            engine::Packet::Query { .. } => PacketType::Query,
            engine::Packet::ProcedureList { .. } => PacketType::ProcedureList,
            engine::Packet::CallProcedure { .. } => PacketType::CallProcedure,
            engine::Packet::StateList { .. } => PacketType::StateList,
            engine::Packet::State { .. } => PacketType::State,
            engine::Packet::UpdateState { .. } => PacketType::UpdateState,
            engine::Packet::Unknown { .. } => PacketType::Unknown,
        };
        Self {
            variant: ptype,
            value: {
                match packet {
                    _ => JsValue::from_serde(&packet).unwrap().into(),
                }
            },
        }
    }
}

use serde_repr::{Deserialize_repr, Serialize_repr};
use std::fmt::Display;

use part::PartProperties;
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[cfg(feature = "net")]
use axum::extract::ws::Message;

#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;

use crate::prelude::*;
use crate::pyproperty;
use crate::universal;
use crate::universal::PortableValue;
use crate::wasmprop;
use crate::Player;

/// An object encapsulating data decoded from JSON.
#[cfg_attr(feature = "logic", pyclass(eq))]
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum Packet {
    Player { data: Player },
    Part { data: PartProperties },
    Question { data: Question },
    QuestionBank { data: QuestionBank },
    Ticker { data: Ticker },
    Timer { data: Timer },
    CommenceSession { data: Credentials },
    AuthStatus { data: AuthenticationStatus },
    Query { data: Query },
    ProcedureList { data: Vec<ProcedureSignature> },
    CallProcedure { data: ProcedureCall },
    StateList { data: Vec<GameState> },
    State { data: GameState },
    UpdateState { data: GameState },
    Unknown { data: String },
    PlayerList { data: Vec<Player> },
    PartList { data: Vec<PartProperties> },
    PlaySound { data: String },
    NextAnimation { data: String },
    LogEntry { data: LogEntry },
}

impl Packet {
    #[deprecated]
    pub fn into_packet<T: 'static>(name: String, data: T) -> Packet {
        // WARNING: HAZMAT SUIT REQUIRED - UNSAFE HELL
        unsafe {
            return match name.as_str() {
                // "Player" if ("Player" == std::any::type_name::<T>()) => Packet::Player(
                //     (&data as &dyn std::any::Any)
                //         .downcast_ref::<Player>()
                //         .expect("Type casting for Packet failed.")
                //         .clone(),
                // ),
                "Player" => Packet::Player {
                    data: std::mem::transmute_copy(&data),
                },
                "Part" => Packet::Part {
                    data: std::mem::transmute_copy(&data),
                },
                "Question" => Packet::Question {
                    data: std::mem::transmute_copy(&data),
                },
                "QuestionBank" => Packet::QuestionBank {
                    data: std::mem::transmute_copy(&data),
                },
                "Ticker" => Packet::Ticker {
                    data: std::mem::transmute_copy(&data),
                },
                "Timer" => Packet::Timer {
                    data: std::mem::transmute_copy(&data),
                },
                "Register" => Packet::CommenceSession {
                    data: std::mem::transmute_copy(&data),
                },
                "AuthStatus" => Packet::AuthStatus {
                    data: std::mem::transmute_copy(&data),
                },
                "RequestResource" => Packet::Query {
                    data: std::mem::transmute_copy(&data),
                },
                "Unknown" => Packet::Unknown {
                    data: std::mem::transmute_copy(&data),
                },

                _ => panic!("Tried to package unknown resource."),
            };
        }
    }
}

impl Display for Packet {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", universal::stringify(self))
    }
}

#[cfg(feature = "logic")]
#[pymethods]
impl Packet {
    pub fn __str__(&self) -> String {
        self.to_string()
    }

    #[pyo3(name = "pack")]
    pub fn py_pack(&self) -> String {
        self.to_string()
    }
}

impl Packet {
    pub fn pack(&self) -> String {
        self.to_string()
    }
}

#[cfg(feature = "wasm")]
impl Packet {
    pub fn wsmsg(&self) -> ws_stream_wasm::WsMessage {
        ws_stream_wasm::WsMessage::Text(self.to_string())
    }
}

#[cfg(feature = "net")]
impl Packet {
    pub fn message(&self) -> Message {
        Message::Text(self.to_string())
    }
}

#[cfg_attr(feature = "logic", pyclass(module = "engine", eq, eq_int))]
#[cfg_attr(feature = "wasm", wasm_bindgen)]
#[derive(Serialize_repr, Deserialize_repr, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "SCREAMING_SNAKE_CASE")]
#[repr(u8)]
#[allow(non_camel_case_types)]
pub enum MediaProperty {
    PLAYING = 0,
    PAUSED = 1,
    SHOWN = 2,
    HIDDEN = 3,
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[cfg_attr(feature = "wasm", wasm_bindgen(skip_typescript))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
/// A callable server-side procedure.
pub struct ProcedureSignature {
    name: String,
    hidden: bool,
    args: Vec<(String, universal::PortableType)>,
}
pyproperty!(ProcedureSignature:name   -> String);
pyproperty!(ProcedureSignature:hidden -> bool);
pyproperty!(
    ProcedureSignature:args -> Vec<(String, universal::PortableType)>
);

#[cfg(feature = "logic")]
#[pymethods]
impl ProcedureSignature {
    #[new]
    pub fn new(
        name: String,
        hidden: bool,
        args: Vec<(String, universal::PortableType)>,
    ) -> PyResult<Self> {
        Ok(Self { name, hidden, args })
    }
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[cfg_attr(feature = "wasm", wasm_bindgen(skip_typescript))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
/// A callable server-side procedure.
pub struct LogEntry {
    timestamp: u128,
    level: i32,
    logger: String,
    content: String,
}
pyproperty!(LogEntry:timestamp:set_timestamp -> u128);
pyproperty!(LogEntry:level:set_level -> i32);
pyproperty!(LogEntry:logger:set_logger -> String);
pyproperty!(LogEntry:content:set_content -> String);

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
/// A value belonging to the game's state.
pub struct GameState {
    pub name: String,
    pub data: PortableValue,
}
pyproperty!(GameState:name:set_name -> String);
pyproperty!(GameState:data:set_data -> PortableValue);

#[cfg(feature = "logic")]
#[pymethods]
impl GameState {
    #[new]
    pub fn new(name: String, data: PortableValue) -> GameState {
        GameState { name, data }
    }
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[cfg_attr(feature = "wasm", wasm_bindgen(skip_typescript))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
/// Authorization request.
pub struct ProcedureCall {
    name: String,
    args: Vec<(String, universal::PortableValue)>,
}
pyproperty!(ProcedureCall:name -> String);
pyproperty!(ProcedureCall:args -> Vec<(String, universal::PortableValue)>);

impl ProcedureCall {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.to_string(),
            args: Vec::new(),
        }
    }

    pub fn append_arg(&mut self, name: &str, v: PortableValue) {
        self.args.push((name.to_string(), v))
    }
}

#[cfg(feature = "logic")]
#[pymethods]
impl ProcedureCall {
    pub fn argno(&self, n: usize) -> universal::PortableValue {
        self.args[n].1.clone()
    }

    fn argname(&self, name: &str) -> Result<PortableValue, pyo3::PyErr> {
        for (n, v) in &self.args {
            if n == name {
                return Ok(v.clone());
            }
        }
        Err(pyo3::exceptions::PyIndexError::new_err(format!(
            "No argument with name {}",
            name
        )))
    }

    pub fn str_argno(&self, n: usize) -> Result<String, PyErr> {
        self.args[n].1.as_str()
    }

    pub fn int_argno(&self, n: usize) -> Result<i32, PyErr> {
        self.args[n].1.as_int()
    }

    pub fn float_argno(&self, n: usize) -> Result<f32, PyErr> {
        self.args[n].1.as_float()
    }

    pub fn str_arg(&self, name: &str) -> Result<String, PyErr> {
        self.argname(name)?.as_str()
    }

    pub fn int_arg(&self, name: &str) -> Result<i32, PyErr> {
        self.argname(name)?.as_int()
    }

    pub fn float_arg(&self, name: &str) -> Result<f32, PyErr> {
        self.argname(name)?.as_float()
    }
}

impl ProcedureSignature {
    pub fn call0(&self) -> ProcedureCall {
        ProcedureCall {
            name: self.name.clone(),
            args: Vec::new(),
        }
    }

    pub fn call1(&self, arg0: PortableValue) -> Result<ProcedureCall, String> {
        if arg0.data_type() != self.args.first().unwrap().1 {
            return Err(String::from("Typecheck failed."));
        }
        Ok(ProcedureCall {
            name: self.name.clone(),
            args: vec![(self.args[0].0.clone(), arg0)],
        })
    }

    pub fn call2(&self, arg0: PortableValue, arg1: PortableValue) -> Result<ProcedureCall, String> {
        if arg0.data_type() != self.args.first().unwrap().1
            || arg1.data_type() != self.args.get(1).unwrap().1
        {
            return Err(String::from("Typecheck failed."));
        }
        Ok(ProcedureCall {
            name: self.name.clone(),
            args: vec![
                (self.args[0].0.clone(), arg0),
                (self.args[1].0.clone(), arg1),
            ],
        })
    }

    pub fn call3(
        &self,
        arg0: PortableValue,
        arg1: PortableValue,
        arg2: PortableValue,
    ) -> Result<ProcedureCall, String> {
        if arg0.data_type() != self.args.first().unwrap().1
            || arg1.data_type() != self.args.get(1).unwrap().1
            || arg2.data_type() != self.args.get(2).unwrap().1
        {
            return Err(String::from("Type check failed"));
        }
        Ok(ProcedureCall {
            name: self.name.clone(),
            args: vec![
                (self.args[0].0.clone(), arg0),
                (self.args[1].0.clone(), arg1),
                (self.args[2].0.clone(), arg2),
            ],
        })
    }
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
/// Authorization request.
pub struct Credentials {
    pub username: String,
    pub access_key: String,
}
pyproperty!(Credentials:username   -> String);
pyproperty!(Credentials:access_key -> String);

impl crate::api::Resource for Credentials {}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
#[cfg_attr(feature = "wasm", wasm_bindgen(skip_typescript))]
/// Authorization request.
pub struct AuthenticationStatus {
    success: bool,
    message: String,
    token: String,
}
pyproperty!(AuthenticationStatus:success -> bool);
pyproperty!(AuthenticationStatus:message -> String);
pyproperty!(AuthenticationStatus:token -> String);
wasmprop!(AuthenticationStatus:wasm_success->success -> bool);
wasmprop!(AuthenticationStatus:wasm_message->message -> String);
wasmprop!(AuthenticationStatus:wasm_token->token -> String);

#[cfg(feature = "logic")]
#[pymethods]
impl AuthenticationStatus {
    #[new]
    pub fn new(success: bool, message: String, token: String) -> Self {
        AuthenticationStatus {
            success,
            message,
            token,
        }
    }
}

impl crate::api::Resource for AuthenticationStatus {}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
#[allow(non_camel_case_types)]
pub enum Query {
    Player { index: String },
    Question { index: usize },
    PartByID { index: usize },
    PartByName { index: String },
    State { index: String },
    PlayerList {},
    QuestionBank {},
    Ticker {},
    Timer {},
    CurrentPart {},
    AvailableProcedures {},
    StateList {},
    PartList {},
    Log { index: i32 },
}

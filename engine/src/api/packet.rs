use part::PartProperties;
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[cfg(feature = "net")]
use axum::extract::ws::Message;

#[cfg(feature = "wasm")]
use js_sys::JSON;

use crate::extract::*;
use crate::Player;

/// An object encapsulating data decoded from JSON.
#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug)]
pub enum Packet {
    Player { data: Player },
    Part { data: PartProperties },
    Question { data: Question },
    QuestionBank { data: QuestionBank },
    Show { data: Show },
    Ticker { data: Ticker },
    Timer { data: Timer },
    Register { data: Credentials },
    AuthStatus { data: AuthenticationStatus },
    RequestResource { data: ResourceRequest },
    ProcedureList { data: Vec<Procedure> },
    CallProcedure { data: ProcedureCall },
    GameState { data: Vec<GameStateValue> },
    UpdateGameState { data: GameStateUpdate },
    Unknown { data: String },
}

impl Packet {
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
                "Show" => Packet::Show {
                    data: std::mem::transmute_copy(&data),
                },
                "Ticker" => Packet::Ticker {
                    data: std::mem::transmute_copy(&data),
                },
                "Timer" => Packet::Timer {
                    data: std::mem::transmute_copy(&data),
                },
                "Register" => Packet::Register {
                    data: std::mem::transmute_copy(&data),
                },
                "AuthStatus" => Packet::AuthStatus {
                    data: std::mem::transmute_copy(&data),
                },
                "RequestResource" => Packet::RequestResource {
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

#[allow(unreachable_code)]
impl ToString for Packet {
    fn to_string(&self) -> String {
        #[cfg(feature = "wasm")]
        return JSON::stringify(&serde_wasm_bindgen::to_value(self).unwrap())
            .unwrap()
            .as_string()
            .unwrap();

        #[cfg(feature = "logic")]
        return serde_json::to_string(self).unwrap();
    }
}

#[cfg(feature = "logic")]
#[pymethods]
impl Packet {
    pub fn __str__(&self) -> String {
        self.to_string()
    }

    pub fn pack(&self) -> String {
        self.to_string()
    }
}

#[cfg(feature = "net")]
impl Packet {
    pub fn message(&self) -> Message {
        Message::Text(self.to_string())
    }
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
/// A callable server-side procedure.
pub struct Procedure {
    pub name: String,
    pub hidden: bool,
    pub args: Vec<(String, PortableValue)>,
}

#[cfg(feature = "logic")]
#[pymethods]
impl Procedure {
    #[new]
    pub fn new(name: String, hidden: bool, args: Vec<(String, String)>) -> PyResult<Self> {
        let mut aargs: Vec<(String, PortableValue)> = Vec::new();
        for (n, t) in args {
            aargs.push((
                n,
                match t.as_str() {
                    "array" => serde_json::Value::Array(Vec::new()),
                    "null" => serde_json::Value::Null,
                    "number" => {
                        serde_json::Value::Number(serde_json::Number::from_f64(0.0).unwrap())
                    }
                    "string" => serde_json::Value::String(String::new()),
                    "object" => serde_json::Value::Object(serde_json::Map::new()),
                    _ => {
                        return Err(pyo3::exceptions::PyTypeError::new_err(format!(
                            "Unknown type: '{}'",
                            t
                        )))
                    }
                },
            ))
        }
        Ok(Self {
            name,
            hidden,
            args: aargs,
        })
    }

    pub fn name(&self) -> String {
        self.name.clone()
    }
    pub fn hidden(&self) -> bool {
        self.hidden
    }
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
/// A value belonging to the game's state.
pub struct GameStateValue {
    pub name: String,
    pub hidden: bool,
    pub data_type: PortableValue,
}

#[cfg(feature = "logic")]
#[pymethods]
impl GameStateValue {
    #[new]
    pub fn new(name: String, hidden: bool, args: String) -> PyResult<Self> {
        Ok(Self {
            name,
            hidden,
            data_type: match args.as_str() {
                "array" => serde_json::Value::Array(Vec::new()),
                "null" => serde_json::Value::Null,
                "number" => serde_json::Value::Number(serde_json::Number::from_f64(0.0).unwrap()),
                "string" => serde_json::Value::String(String::new()),
                "object" => serde_json::Value::Object(serde_json::Map::new()),
                _ => {
                    return Err(pyo3::exceptions::PyTypeError::new_err(format!(
                        "Unknown type: '{}'",
                        args
                    )))
                }
            },
        })
    }

    pub fn name(&self) -> String {
        self.name.clone()
    }
    pub fn hidden(&self) -> bool {
        self.hidden
    }
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
/// A value belonging to the game's state.
pub struct GameStateUpdate {
    pub name: String,
    pub data: String,
}

#[cfg_attr(feature = "logic", pymethods)]
impl GameStateUpdate {
    pub fn name(&self) -> String {
        self.name.clone()
    }

    pub fn data(&self) -> String {
        self.data.clone()
    }
}

#[cfg(feature = "logic")]
pub type PortableValue = serde_json::Value;
#[cfg(not(feature = "logic"))]
#[cfg(feature = "wasm")]
pub type PortableValue = wasm_bindgen::JsValue;

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
/// Authorization request.
pub struct ProcedureCall {
    pub name: String,
    pub args: Vec<(String, String)>,
}

#[cfg_attr(feature = "logic", pymethods)]
impl ProcedureCall {
    pub fn name(&self) -> String {
        self.name.clone()
    }

    pub fn args(&self) -> Vec<(String, String)> {
        self.args.clone()
    }
}

#[cfg(feature = "logic")]
impl Procedure {
    pub fn call0(&self) -> ProcedureCall {
        ProcedureCall {
            name: self.name.clone(),
            args: Vec::new(),
        }
    }

    pub fn call1(&self, arg0: serde_json::Value) -> Result<ProcedureCall, ()> {
        if std::mem::discriminant(&arg0) != std::mem::discriminant(&(&self.args[0].1)) {
            return Err(());
        }
        Ok(ProcedureCall {
            name: self.name.clone(),
            args: vec![(
                self.args[0].0.clone(),
                serde_json::to_string(&arg0).unwrap(),
            )],
        })
    }

    pub fn call2(
        &self,
        arg0: serde_json::Value,
        arg1: serde_json::Value,
    ) -> Result<ProcedureCall, ()> {
        if std::mem::discriminant(&arg0) != std::mem::discriminant(&(&self.args[0].1))
            || std::mem::discriminant(&arg1) != std::mem::discriminant(&(&self.args[1].1))
        {
            return Err(());
        }
        Ok(ProcedureCall {
            name: self.name.clone(),
            args: vec![
                (
                    self.args[0].0.clone(),
                    serde_json::to_string(&arg0).unwrap(),
                ),
                (
                    self.args[1].0.clone(),
                    serde_json::to_string(&arg1).unwrap(),
                ),
            ],
        })
    }

    pub fn call3(
        &self,
        arg0: serde_json::Value,
        arg1: serde_json::Value,
        arg2: serde_json::Value,
    ) -> Result<ProcedureCall, ()> {
        if std::mem::discriminant(&arg0) != std::mem::discriminant(&(&self.args[0].1))
            || std::mem::discriminant(&arg1) != std::mem::discriminant(&(&self.args[1].1))
            || std::mem::discriminant(&arg2) != std::mem::discriminant(&(&self.args[2].1))
        {
            return Err(());
        }
        Ok(ProcedureCall {
            name: self.name.clone(),
            args: vec![
                (
                    self.args[0].0.clone(),
                    serde_json::to_string(&arg0).unwrap(),
                ),
                (
                    self.args[1].0.clone(),
                    serde_json::to_string(&arg1).unwrap(),
                ),
                (
                    self.args[2].0.clone(),
                    serde_json::to_string(&arg2).unwrap(),
                ),
            ],
        })
    }
}

#[cfg(not(feature = "logic"))]
#[cfg(feature = "wasm")]
impl Procedure {
    pub fn call0(&self) -> ProcedureCall {
        ProcedureCall {
            name: self.name.clone(),
            args: Vec::new(),
        }
    }

    pub fn call1(&self, arg0: wasm_bindgen::JsValue) -> Result<ProcedureCall, ()> {
        if arg0.js_typeof() != self.args[0].1.js_typeof() {
            return Err(());
        }
        Ok(ProcedureCall {
            name: self.name.clone(),
            args: vec![(
                self.args[0].0.clone(),
                js_sys::JSON::stringify(&arg0).unwrap(),
            )
                .to_string()],
        })
    }

    pub fn call2(
        &self,
        arg0: wasm_bindgen::JsValue,
        arg1: wasm_bindgen::JsValue,
    ) -> Result<ProcedureCall, ()> {
        if arg0.js_typeof() != self.args[0].1.js_typeof()
            || arg1.js_typeof() != self.args[1].1.js_typeof()
        {
            return Err(());
        }
        Ok(ProcedureCall {
            name: self.name.clone(),
            args: vec![
                (
                    self.args[0].0.clone(),
                    js_sys::JSON::stringify(&arg0).unwrap().to_string(),
                ),
                (
                    self.args[1].0.clone(),
                    js_sys::JSON::stringify(&arg1).unwrap().to_string(),
                ),
            ],
        })
    }

    pub fn call3(
        &self,
        arg0: wasm_bindgen::JsValue,
        arg1: wasm_bindgen::JsValue,
        arg2: wasm_bindgen::JsValue,
    ) -> Result<ProcedureCall, ()> {
        if arg0.js_typeof() != self.args[0].1.js_typeof()
            || arg1.js_typeof() != self.args[1].1.js_typeof()
            || arg2.js_typeof() != self.args[2].1.js_typeof()
        {
            return Err(());
        }
        Ok(ProcedureCall {
            name: self.name.clone(),
            args: vec![
                (
                    self.args[0].0.clone(),
                    js_sys::JSON::stringify(&arg0).unwrap().to_string(),
                ),
                (
                    self.args[1].0.clone(),
                    js_sys::JSON::stringify(&arg1).unwrap().to_string(),
                ),
                (
                    self.args[2].0.clone(),
                    js_sys::JSON::stringify(&arg2).unwrap().to_string(),
                ),
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

impl crate::api::Resource for Credentials {}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
/// Authorization request.
pub struct AuthenticationStatus {
    pub success: bool,
    pub message: String,
}
#[cfg(feature = "logic")]
#[pymethods]
impl AuthenticationStatus {
    #[new]
    pub fn new(success: bool, message: String) -> Self {
        AuthenticationStatus { success, message }
    }
}

impl crate::api::Resource for AuthenticationStatus {}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub enum ResourceRequest {
    Player { index: String },
    Question { index: usize },
    PartByID { index: usize },
    PartByName { index: String },
    QuestionBank {},
    Show {},
    Ticker {},
    Timer {},
    CurrentPart {},
    AvailableProcedures {},
    GameState {},
}

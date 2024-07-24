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
}

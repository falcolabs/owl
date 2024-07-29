#[allow(unused)]
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[cfg(feature = "logic")]
use crate::net::wspy::IOHandle;

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Clone, Debug)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct Player {
    pub identifier: String,
    pub name: String,
    pub score: i32,
    #[serde(skip)]
    #[cfg(feature = "logic")]
    pub handle: Option<IOHandle>,
}

impl Player {
    pub fn new(identifier: String, name: String, score: i32) -> Self {
        Player {
            identifier,
            name,
            score,
            #[cfg(feature = "logic")]
            handle: Option::None,
        }
    }
}

impl crate::api::Resource for Player {}

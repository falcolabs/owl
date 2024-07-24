#[allow(unused)]
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::time::SystemTime;

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Clone, Copy, Debug)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct Ticker {
    pub last_tick: SystemTime,
}

unsafe impl Send for Ticker {}
unsafe impl Sync for Ticker {}
impl crate::api::Resource for Ticker {}

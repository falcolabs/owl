#[cfg(feature = "logic")]
use pyo3::prelude::*;
#[allow(unused)]
use serde::{Deserialize, Serialize};
use std::time::{Duration, SystemTime};

use crate::pyproperty;

#[cfg_attr(feature = "logic", pyclass)]
#[derive(Serialize, Deserialize, Clone, Debug, Eq, PartialEq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct Timer {
    pub start_time: SystemTime,
    pub paused_time: SystemTime,
    pub paused_duration: Duration,
    pub is_paused: bool,
}
pyproperty!(Timer:start_time -> SystemTime);
pyproperty!(Timer:paused_time -> SystemTime);
pyproperty!(Timer:paused_duration -> Duration);
pyproperty!(Timer:is_paused -> bool);

impl crate::api::Resource for Timer {}

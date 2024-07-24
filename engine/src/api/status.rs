#[allow(unused)]
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Clone, Copy, Debug, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "UPPERCASE")]
pub enum Status {
    /// Running as usual.
    RUNNING,
    /// Skipping the current part and jump on the next part.
    SKIP,
    /// Stopping the current part and returning to the previous one.
    REWIND,
    /// Pause the current part.
    PAUSED,
    /// The show is stopping.
    STOP,
}

pub trait State: crate::api::Resource {}
impl crate::api::Resource for Status {}

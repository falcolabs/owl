#[cfg(feature = "api")]
pub mod api;
#[cfg(feature = "logging")]
pub mod logging;
#[cfg(feature = "logic")]
pub mod logic;

#[cfg(feature = "net")]
pub mod net;

pub mod extract;
pub use extract::*;
#[cfg(feature = "logic")]
use pyo3::prelude::*;

#[cfg(feature = "logic")]
#[pymodule]
mod engine {
    #[pymodule_export]
    use crate::extract::{
        AuthenticationStatus, Credentials, Packet, Part, PartProperties, Player, Question,
        QuestionBank, ResourceRequest, Show, Status, Ticker, Timer,
    };

    #[pymodule_export]
    use crate::net::wspy::{IOHandle, RawRequest};

    #[pymodule_export]
    use crate::logging::{
        color::{mccolor, mccolor_esc, Color},
        logger::{py_debug, py_error, py_info, py_warning, Level},
    };
}

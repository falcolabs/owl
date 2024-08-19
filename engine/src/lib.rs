#[cfg(feature = "api")]
pub mod api;
#[cfg(feature = "logging")]
pub mod logging;
#[cfg(feature = "logic")]
pub mod logic;

pub mod universal;

#[cfg(feature = "net")]
pub mod net;

pub mod prelude;
pub use prelude::*;
#[cfg(feature = "logic")]
use pyo3::prelude::*;

#[cfg(feature = "logic")]
#[pymodule]
mod engine {
    #[pymodule_export]
    use crate::prelude::{
        AuthenticationStatus, Credentials, GameStatePrototype, GameStateUpdate, Packet, Part,
        PartProperties, Player, ProcedureCall, ProcedureSignature, Query, Question, QuestionBank,
        Show, Status, Ticker, Timer,
    };

    #[pymodule_export]
    use crate::universal::{PortableType, PortableValue};

    #[pymodule_export]
    use crate::net::wspy::{IOHandle, RawRequest};

    #[pymodule_export]
    use crate::logging::{
        color::{mccolor, mccolor_esc, Color},
        logger::{py_debug, py_error, py_info, py_warning, Level, set_log_level},
    };
}

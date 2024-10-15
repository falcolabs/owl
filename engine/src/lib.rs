/**
 *  engine, a data serialization and syncronization for owl.
 *  Copyright (C) 2024 Team Falco
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

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
        AuthenticationStatus, Credentials, GameState, LogEntry, MediaContent, Packet, Part,
        PartProperties, Player, ProcedureCall, ProcedureSignature, Query, Question, QuestionBank,
        Status, Ticker, Timer,
    };

    #[pymodule_export]
    use crate::universal::{PortableType, PortableValue};

    #[pymodule_export]
    use crate::net::wspy::{IOHandle, RawRequest};

    #[pymodule_export]
    use crate::logging::{
        color::{mccolor, mccolor_esc, Color},
        logger::{py_debug, py_error, py_info, py_warning, set_log_level, Level},
    };

    #[pymodule_export]
    use crate::logic::show::ws_task;
}

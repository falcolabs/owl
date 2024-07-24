use crate::extract::{Part, Player, QuestionBank, Ticker, Timer};
#[allow(unused)]
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

/// Represents a show's properties.
#[cfg_attr(feature = "logic", pyclass(module = "engine", subclass))]
#[allow(unused)]
#[derive(Serialize, Deserialize, Clone, Debug)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct Show {
    /// The name of the show.
    pub name: String,
    /// The parts included in the show.
    #[serde(skip)]
    pub parts: Vec<Part>,
    /// The show's tick speed.
    pub tick_speed: u32,
    /// The current part index.
    pub current_part: usize,
    /// The players present
    pub players: Vec<Player>,
    /// All the questions the show contains
    pub qbank: QuestionBank,
    /// The show's ticker
    pub ticker: Ticker,
    /// The show's timer
    pub timer: Timer,
}

unsafe impl Send for Show {}
unsafe impl Sync for Show {}
impl crate::api::Resource for Show {}

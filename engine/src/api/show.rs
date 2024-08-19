use crate::{
    prelude::{Part, Player, QuestionBank, Ticker, Timer},
    pyproperty,
};
#[allow(unused)]
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

/// Represents a show's properties.
#[cfg_attr(feature = "logic", pyclass(module = "engine", subclass))]
#[allow(unused)]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
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
pyproperty!(Show:name         : set_name         -> String       );
pyproperty!(Show:parts        : set_parts        -> Vec<Part>    );
pyproperty!(Show:tick_speed   : set_tick_speed   -> u32          );
pyproperty!(Show:current_part : set_current_part -> usize        );
pyproperty!(Show:players      : set_players      -> Vec<Player>  );
pyproperty!(Show:qbank        : set_qbank        -> QuestionBank );
pyproperty!(Show:ticker       : set_ticker       -> Ticker       );
pyproperty!(Show:timer        : set_timer        -> Timer        );

unsafe impl Send for Show {}
unsafe impl Sync for Show {}
impl crate::api::Resource for Show {}

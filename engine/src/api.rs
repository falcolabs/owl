//! APIs and basic data structures in use for a show.
//! Often, they are used along with `serde` to send data
//! and sync them with WebSockets; however, game logic are
//! still present if one ever need it.

pub mod packet;
pub mod part;
pub mod player;
pub mod question;
pub mod show;
pub mod status;
pub mod tick;
pub mod timer;

pub use {
    self::packet::*,
    self::part::{Part, PartProperties},
    self::player::Player,
    self::question::{Question, QuestionBank},
    self::show::Show,
    self::status::Status,
    self::tick::Ticker,
    self::timer::Timer,
};

pub trait Resource {
    fn resource(&self) -> String {
        std::any::type_name::<Self>().to_string()
    }
}

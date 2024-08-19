//! Module dealing with server-client communications,
//! through the ground breaking novel cutting-edge revolutionary
//! lighting fast easy to use lightweight technology of WebSocket.
pub mod webservice_ws;
pub mod wspy;

pub use self::webservice_ws::{Callback, MessageHandler};

pub use crate::api::tick::Ticker;
use pyo3::prelude::*;
use std::{
    thread,
    time::{Duration, SystemTime},
};

impl Default for Ticker {
    fn default() -> Self {
        Self::new()
    }
}

#[pymethods]
impl Ticker {
    #[new]
    pub fn new() -> Ticker {
        Ticker {
            last_tick: SystemTime::now(),
        }
    }
    /// Ensures the tick speed is met.
    pub fn tick(&mut self, tick_speed: u32) {
        // let code_runtime = SystemTime::now()
        // .duration_since(self.last_tick)
        // .expect("Error when calculating time elapsed for regulating tick speed");
        // let sleep_dur = Duration::from_millis(((1_f32 / tick_speed as f32) * 1000_f32) as u64);
        thread::sleep(Duration::from_millis(
            ((1_f32 / tick_speed as f32) * 1000_f32) as u64,
        ));
        // self.last_tick = SystemTime::now();
    }
}

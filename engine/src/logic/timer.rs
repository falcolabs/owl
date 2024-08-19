pub use crate::api::Timer;

use pyo3::prelude::*;
use std::time::{Duration, SystemTime};

#[pymethods]
impl Timer {
    /// Creates a new timer, which starts immidiately after creation.
    #[cfg(feature = "logic")]
    #[new]
    pub fn new() -> Timer {
        Timer {
            start_time: SystemTime::now(),
            paused_duration: Duration::new(0, 0),
            paused_time: SystemTime::now(),
            is_paused: false,
        }
    }

    /// Pauses the timer.
    pub fn pause(&mut self) {
        if !self.is_paused {
            self.paused_time = SystemTime::now();
            self.is_paused = true
        }
    }
    /// Resumes the timer.
    pub fn resume(&mut self) {
        if self.is_paused {
            self.paused_duration += SystemTime::now()
                .duration_since(self.paused_time)
                .expect("We time travelled. Congrats!");
            self.is_paused = false;
        }
    }

    /// Gets the time elapsed from the calling of `start()`,
    /// minus the pauses.
    pub fn time_elapsed(&self) -> Duration {
        let base_dur: Duration;
        if self.is_paused {
            base_dur = self
                .start_time
                .duration_since(self.paused_time)
                .expect("We time travelled. Congrats.");
        } else {
            base_dur = SystemTime::now()
                .duration_since(self.start_time)
                .expect("We time travelled. Congrats.");
        }
        base_dur - self.paused_duration
    }
}
#[allow(unused)]
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::time::{Duration, SystemTime};

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Clone, Debug)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct Timer {
    pub start_time: SystemTime,
    pub paused_time: SystemTime,
    pub paused_duration: Duration,
    pub is_paused: bool,
}

impl crate::api::Resource for Timer {}

// The Timer implementation is kept in crate `api`
// as it is also needed for the front end.
#[cfg_attr(feature = "logic", pymethods)]
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

#[cfg(not(feature = "logic"))]
impl Timer {
    pub fn new() -> Timer {
        Timer {
            start_time: SystemTime::now(),
            paused_duration: Duration::new(0, 0),
            paused_time: SystemTime::now(),
            is_paused: false,
        }
    }
}

use engine::wasmprop;
use serde::{Deserialize, Serialize};
use std::time::{Duration, SystemTime};
use wasm_bindgen::prelude::*;

#[wasm_bindgen(skip_typescript)]
#[derive(Debug, Serialize, Deserialize, Clone, Copy)]
#[allow(dead_code)]
pub struct Timer {
    start_time: SystemTime,
    paused_time: SystemTime,
    paused_duration: Duration,
    is_paused: bool,
}
wasmprop!(Timer:start_time      :set_start_time      -> SystemTime);
wasmprop!(Timer:paused_time     :set_paused_time     -> SystemTime);
wasmprop!(Timer:paused_duration :set_paused_duration -> Duration);
wasmprop!(Timer:is_paused       :set_is_paused       -> bool);

#[wasm_bindgen]
impl Timer {
    #[wasm_bindgen(constructor)]
    pub fn constructor() -> Timer {
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
    #[wasm_bindgen(js_name = elapsedSecs)]
    pub fn elapsed_secs(&self) -> f32 {
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
        (base_dur - self.paused_duration).as_secs_f32()
    }
}

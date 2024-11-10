use engine::wasmprop;
use gloo_utils::format::JsValueSerdeExt;
use serde::{Deserialize, Serialize};
use wasm_bindgen::prelude::*;
use web_time::{Duration, SystemTime};

#[wasm_bindgen(skip_typescript, inspectable)]
#[derive(Debug, Serialize, Deserialize, Clone, Copy)]
#[allow(dead_code)]
#[serde(rename_all = "camelCase")]
pub struct Timer {
    start_time: SystemTime,
    paused_time: SystemTime,
    paused_duration: Duration,
    is_paused: bool,
}
wasmprop!(Timer:wasm_get_start_time     ,wasm_set_start_time      -> start_time      -> SystemTime);
wasmprop!(Timer:wasm_get_paused_time    ,wasm_set_paused_time     -> paused_time     -> SystemTime);
wasmprop!(Timer:wasm_get_paused_duration,wasm_set_paused_duration -> paused_duration -> Duration);
wasmprop!(Timer:wasm_get_is_paused      ,wasm_set_is_paused       -> is_paused       -> bool);

#[wasm_bindgen]
impl Timer {
    #[wasm_bindgen(constructor)]
    pub fn constructor() -> Timer {
        // This has to be done, as one of the syscalls might return
        // sooner, despite being scheduled first.
        let now = SystemTime::now();
        Timer {
            start_time: now,
            paused_duration: Duration::new(0, 0),
            paused_time: now,
            is_paused: true,
        }
    }

    pub fn from(obj: js_sys::Object) -> Timer {
        <js_sys::Object as Into<JsValue>>::into(obj)
            .into_serde()
            .unwrap()
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
                .paused_time
                .duration_since(self.start_time)
                .expect("We time travelled. Congrats");
        } else {
            base_dur = SystemTime::now()
                .duration_since(self.start_time)
                .expect("We time travelled. Congrats");
        }
        (base_dur - self.paused_duration).as_secs_f32()
    }

    #[wasm_bindgen(js_name = isPaused)]
    pub fn is_paused(&self) -> bool {
        self.is_paused
    }

    pub fn pack(&self) -> String {
        serde_json::to_string(self).unwrap()
    }
}

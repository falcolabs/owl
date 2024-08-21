use core::panic;

pub use crate::api::Show;
use crate::prelude::*;
use pyo3::prelude::*;

#[allow(unused)]
#[pymethods]
impl Show {
    #[staticmethod]
    pub fn ws_task(listen_on: String, serve_on: String, static_dir: String, call_hook: Py<PyAny>) {
        let (tx, mut rx) = std::sync::mpsc::channel::<crate::net::wspy::RawRequest>();
        std::thread::spawn(move || {
            crate::net::wspy::start_webservice(tx, listen_on, serve_on, static_dir);
        });

        std::thread::spawn(move || {
            while let Ok(req) = rx.recv() {
                Python::with_gil(|py| match call_hook.bind(py).call1((req,)) {
                    Ok(_) => {}
                    Err(exp) => {
                        exp.print(py);
                        panic!("Python exception raised. See error above.")
                    }
                })
            }
        });
    }

    #[new]
    pub fn new(
        name: String,
        mut parts: Vec<Part>,
        players: Vec<Player>,
        tick_speed: u32,
        question_bank: QuestionBank,
    ) -> Self {
        Self {
            name,
            parts,
            players,
            tick_speed,
            current_part: 0,
            qbank: question_bank,
            ticker: Ticker::new(),
            timer: Timer::new(),
        }
    }
}

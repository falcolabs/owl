use core::panic;
use std::{thread, time::Duration};

use pyo3::prelude::*;

use crate::{net::wspy::Notifier, Ticker};

#[pyfunction]
pub fn ws_task(
    listen_on: String,
    serve_on: String,
    static_dir: String,
    tick_speed: u32,
    tick_hook: Py<PyAny>,
) {
    let (tx, rx) = std::sync::mpsc::channel::<crate::net::wspy::Notifier>();
    let tx1 = tx.clone();
    std::thread::spawn(move || {
        crate::net::wspy::start_webservice(tx1, listen_on, serve_on, static_dir);
    });
    let tx2 = tx.clone();
    std::thread::spawn(move || {
        // TODO - this is intentional wait time
        thread::sleep(Duration::from_secs(3));
        let mut ticker = Ticker::new();
        loop {
            ticker.tick(tick_speed);
            tx2.send(Notifier::ExecuteTick).unwrap();
        }
    });

    std::thread::spawn(move || {
        while let Ok(req) = rx.recv() {
            Python::with_gil(|py| {
                if let Notifier::RawRequest(raw_req) = req {
                    match tick_hook.bind(py).call1((true, raw_req)) {
                        Ok(_) => {}
                        Err(exp) => {
                            exp.print(py);
                            panic!("Python exception raised. See error above.")
                        }
                    }
                } else {
                    match tick_hook.bind(py).call1((false, "")) {
                        Ok(_) => {}
                        Err(exp) => {
                            exp.print(py);
                            panic!("Python exception raised. See error above.")
                        }
                    }
                }
            })
        }
    });
}

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
    time_hook: Py<PyAny>,
) {
    let (tx_main, rx_main) = std::sync::mpsc::channel::<crate::net::wspy::Notifier>();
    let (tx_time, rx_time) = std::sync::mpsc::channel::<crate::net::wspy::Notifier>();
    let tx1_main = tx_main.clone();
    let tx1_time = tx_time.clone();
    std::thread::spawn(move || {
        crate::net::wspy::start_webservice(tx1_main, tx1_time, listen_on, serve_on, static_dir);
    });
    let tx2 = tx_main.clone();
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
        while let Ok(req) = rx_main.recv() {
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
    std::thread::spawn(move || {
        while let Ok(req) = rx_time.recv() {
            Python::with_gil(|py| {
                if let Notifier::RawRequest(raw_req) = req {
                    match time_hook.bind(py).call1((raw_req,)) {
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

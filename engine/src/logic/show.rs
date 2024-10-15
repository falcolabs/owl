use core::panic;

use pyo3::prelude::*;

#[pyfunction]
pub fn ws_task(listen_on: String, serve_on: String, static_dir: String, call_hook: Py<PyAny>) {
    let (tx, rx) = std::sync::mpsc::channel::<crate::net::wspy::RawRequest>();
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

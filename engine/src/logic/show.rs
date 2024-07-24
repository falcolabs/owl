pub use crate::api::Show;
use crate::extract::*;
use pyo3::prelude::*;

#[allow(unused)]
#[pymethods]
impl Show {
    /// Starts the show. This is a blocking function, and will only stop
    /// when the show is terminated by the user.
    /// **This function contains an intentional memory leak.**
    ///
    /// # Arguments
    /// * `listen_on` - the host and port for the server to listen on.
    ///                 resource will be hosted on `/`, WebSocket PI on `/harlem`
    /// * `serve_dir` - where the static content will be hosted at.
    ///                 May contain unsolicited WebAssembly.
    /// * `static_dir` - where the static content lives. Should contain `404.html`.
    ///
    /// # Examples
    /// ```
    /// // This function will block until the show ends.
    /// show.start("localhost:6942", "./public", "./static");
    /// ```
    ///
    // pub fn start(
    //     slf: PyRefMut<Show>,

    //     listen_on: String,
    //     serve_on: String,
    //     static_dir: String,
    //     callback: Py<PyAny>,
    // ) {
    // Evil GIL grabber
    // Python::with_gil(|_| {
    //     let mut rt = tokio::runtime::Runtime::new().unwrap();
    //     logging::info("Starting show...");
    //     let (kill_send, mut kill_recv) = std::sync::mpsc::channel::<bool>();
    //     let (tx, mut rx) = std::sync::mpsc::channel::<crate::net::wspy::RawRequest>();

    //     let nethandle = rt.spawn(async move {
    //         tokio::time::sleep(GIL_WAIT_SLEEP).await;
    //         logging::info("Starting webserver thread...");
    // net::wspy::start_webservice(tx, listen_on, serve_on, static_dir).await
    //     });

    //     let showhandle = rt.spawn({
    //         let mut show = slf.clone();
    //         async move {
    //             tokio::time::sleep(GIL_WAIT_SLEEP).await;
    //             logging::info("Starting show thread...");
    //             let py = unsafe_getpy();
    //             show.ticker = Ticker::new();
    //             let tick_speed = show.tick_speed;
    //             let current_part = show.current_part;
    //             let mut last_current_part = current_part;
    //             let mut part = show.parts.get(current_part).unwrap().clone();

    //             loop {
    //                 py.check_signals().expect("Killing threads...");
    //                 {
    //                     show.ticker.tick(tick_speed);
    //                     if current_part != last_current_part {
    //                         part = show.parts.get(current_part).unwrap().clone();
    //                         last_current_part = current_part;
    //                     }
    //                 }
    //                 let mut result = Status::RUNNING;
    //                 result = part
    //                     .update_hook()
    //                     .call1(py, (show.clone(),))
    //                     .unwrap()
    //                     .extract(py)
    //                     .unwrap();

    //                 match result {
    //                     Status::STOP => {
    //                         logging::info("Show is stopped by show logic.");
    //                         std::process::exit(0);
    //                     }
    //                     Status::SKIP => {
    //                         if show.current_part >= show.parts.len() {
    //                             logging::info("There are no more parts in the show. Stopping.");
    //                             std::process::exit(0);
    //                         }
    //                         show.current_part += 1;
    //                     }
    //                     Status::REWIND => {
    //                         if show.current_part <= 0 {
    //                             logging::info(
    //                             "There are no more parts before the current part. Stopping.",
    //                         );
    //                             std::process::exit(0);
    //                         }
    //                         show.current_part -= 1;
    //                     }
    //                     _ => {}
    //                 }
    //             }
    //         }
    //     });
    //     rt.block_on(async move {
    //         let local = tokio::task::LocalSet::new();
    //         let messenger = local.spawn_local(async move {
    //             let py = unsafe_getpy();
    //             let asyncio = py.import_bound("asyncio").unwrap();
    //             let evloop = asyncio.call_method0("get_event_loop").unwrap().unbind();
    //             logging::info("messenger is running");
    //             while let Ok(request) = rx.recv() {
    //                 logging::info("Passing request to Python");
    //                 let coroutine = callback
    //                     .bind(py)
    //                     .call1((request,))
    //                     .expect("Calling network handler hook failed.");
    //                 if let Err(stacktrace) = evloop
    //                     .bind(py)
    //                     .call_method1("run_until_complete", (coroutine,))
    //                 {
    //                     stacktrace.print(py);
    //                     panic!();
    //                 }
    //             }
    //         });
    //         local.spawn_local(async move {
    //             let py = unsafe_getpy();
    //             logging::info("Starting watchdawg thread...");

    //             loop {
    //                 tokio::time::sleep(Duration::from_millis(500));
    //                 match py.check_signals() {
    //                     Err(_) => {
    //                         logging::info("KeyboardInterrupt received. Killing threads...");
    //                         kill_send.send(true).unwrap();
    //                         nethandle.abort();
    //                         showhandle.abort();
    //                         messenger.abort();
    //                         logging::success("All threads killed. Goodbye!");
    //                         exit(0);
    //                         break;
    //                     }
    //                     Ok(_) => {}
    //                 };
    //             }
    //         });
    //         local.await;
    //     });
    // });
    // }

    // pub fn start(
    //     mut show: Arc<Mutex<Show>>,
    //     listen_on: String,
    //     serve_dir: String,
    //     static_dir: String,
    //     callback: Box<net::MessageHandler>,
    // ) {
    //     loop {
    //         // Limiting `show.blocking_lock()` and `sc` scope
    //         {
    //             let part = parts.get_mut(show.blocking_lock().current_part).unwrap();
    //             show.blocking_lock()
    //                 .ticker
    //                 .tick(show.blocking_lock().tick_speed);
    //             result = part.on_update(Arc::clone(&show));
    //             match result {
    //             Status::STOP => {
    //                 logging::info("Show is stopped by show logic.");
    //                 std::process::exit(0);
    //             }
    //             Status::SKIP => {
    //                 if show.blocking_lock().current_part >= show.blocking_lock().parts.len() {
    //                     logging::info("There are no more parts in the show. Stopping.");
    //                     std::process::exit(0);
    //                 }
    //                 show.blocking_lock().current_part += 1;
    //             }
    //             Status::REWIND => {
    //                 if show.blocking_lock().current_part <= 0 {
    //                     logging::info("There are no more parts before the current part. Stopping.");
    //                     std::process::exit(0);
    //                 }
    //                 show.blocking_lock().current_part -= 1;
    //             }
    //             _ => {}
    //         }
    //         }
    //
    //     }
    // }

    #[staticmethod]
    pub fn ws_task(listen_on: String, serve_on: String, static_dir: String, call_hook: Py<PyAny>) {
        let test = crate::api::Packet::Part {
            data: PartProperties {
                name: String::from("auth"),
            },
        };
        println!("{:#?}", test.pack());
        println!(
            "{:#?}",
            serde_json::from_str::<crate::api::Packet>(test.pack().as_str())
        );

        let (tx, mut rx) = std::sync::mpsc::channel::<crate::net::wspy::RawRequest>();
        std::thread::spawn(move || {
            crate::net::wspy::start_webservice(tx, listen_on, serve_on, static_dir);
        });

        std::thread::spawn(move || {
            while let Ok(req) = rx.recv() {
                Python::with_gil(|py| {
                    call_hook.bind(py).call1((req,)).unwrap();
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

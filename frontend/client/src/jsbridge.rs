use wasm_bindgen::prelude::*;

#[wasm_bindgen]
extern "C" {
    /// Calls JavaScript `console.log()`.
    /// The syntax is simillar to that of
    /// `format!()` or `println!()`.
    #[wasm_bindgen(js_namespace = console)]
    pub fn log(s: &str);
}

/// Calls JavaScript `console.log()`.
/// The syntax is simillar to that of
/// `format!()` or `println!()`.
#[macro_export]
macro_rules! console_log {
    ($($t:tt)*) => (crate::jsbridge::log(&format_args!($($t)*).to_string()))
}

pub fn set_panic_hook() {
    console_error_panic_hook::set_once();
}

pub async fn sleep(milis: i32) {
    let promise = js_sys::Promise::new(&mut |resolve, _| {
        web_sys::window()
            .unwrap()
            .set_timeout_with_callback_and_timeout_and_arguments_0(&resolve, milis)
            .expect("Cannot setup timeout.");
    });
    wasm_bindgen_futures::JsFuture::from(promise)
        .await
        .expect("You cannot sleep now, there is monster nearny");
}

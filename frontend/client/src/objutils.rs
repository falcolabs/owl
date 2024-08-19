use js_sys::Object;
use wasm_bindgen::JsCast;
use wasm_bindgen::JsValue;

pub fn extractjs<T: JsCast>(obj: &Object, name: &str) -> T {
    js_sys::Reflect::get(obj, &JsValue::from_str(name))
        .expect(
            format!(
                "Error when extracting property `{}` from `{:#?}`",
                name, obj
            )
            .as_str(),
        )
        .dyn_into()
        .expect("Unable to cast JsValue when extracting from JS")
}

#[macro_export]
macro_rules! property_getter {
    ($for:ident, $name:ident, $type:ty) => {
        #[wasm_bindgen]
        impl $for {
            #[wasm_bindgen(getter)]
            pub fn $name(&self) -> $type {
                self.$name.clone()
            }
        }
    };
}
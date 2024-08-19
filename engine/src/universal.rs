//! Bindings for types and methods usable and
//! transferable to and from JS, WASM, Python and Rust.

#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;

#[cfg(feature = "logic")]
use pyo3::prelude::*;

#[macro_export]
macro_rules! pyproperty {
    ($type:ty:$name:ident -> $dt:ty) => {
        #[cfg(feature = "logic")]
        #[pymethods]
        impl $type {
            #[getter($name)]
            pub fn $name(&self) -> $dt {
                self.$name.clone()
            }
        }
    };
    ($type:ty:$name:ident:$set_name:ident -> $dt:ty) => {
        #[cfg(feature = "logic")]
        #[pymethods]
        impl $type {
            #[getter($name)]
            fn $name(&self) -> $dt {
                self.$name.clone()
            }

            #[setter($name)]
            fn $set_name(&mut self, new_value: $dt) {
                self.$name = new_value
            }
        }
    };
}

#[macro_export]
macro_rules! wasmprop {
    ($type:ty:$name:ident -> $dt:ty) => {
        #[cfg(feature = "wasm")]
        #[wasm_bindgen]
        impl $type {
            #[wasm_bindgen(getter)]
            pub fn $name(&self) -> $dt {
                self.$name.clone()
            }
        }
    };
    ($type:ty:$name:ident:$set_name:ident -> $dt:ty) => {
        #[cfg(feature = "wasm")]
        #[wasm_bindgen]
        impl $type {
            #[wasm_bindgen(getter)]
            pub fn $name(&self) -> $dt {
                self.$name.clone()
            }

            #[wasm_bindgen(setter)]
            pub fn $set_name(&mut self, new_value: $dt) {
                self.$name = new_value
            }
        }
    };
}

#[cfg(feature = "wasm")]
#[allow(dead_code)]
mod wasm {
    use serde_wasm_bindgen;

    pub fn stringify<T: serde::Serialize + std::fmt::Debug>(sth: &T) -> String {
        js_sys::JSON::stringify(
            &serde_wasm_bindgen::to_value(sth)
                .expect(format!("Unable to serialize T, serde-wasm error: {:#?}", sth).as_str()),
        )
        .expect(
            format!(
                "Unable to serialize T, got JSON.stringify() error: {:#?}",
                sth
            )
            .as_str(),
        )
        .as_string()
        .unwrap()
    }

    pub fn parse<'a, T: serde::de::DeserializeOwned>(data: &'a str) -> T {
        serde_wasm_bindgen::from_value(js_sys::JSON::parse(data).expect("JSON.parse() error"))
            .unwrap()
    }
}

#[cfg(feature = "logic")]
#[allow(dead_code)]
mod logic {
    pub fn stringify<T: serde::Serialize>(sth: &T) -> String {
        serde_json::to_string(sth).expect("serde serialization error")
    }

    pub fn parse<'a, T: serde::de::DeserializeOwned>(data: &'a str) -> T {
        serde_json::from_str(data).expect("serde deserialization error")
    }
}

#[cfg_attr(feature = "logic", pyclass(eq, eq_int))]
#[cfg_attr(feature = "wasm", wasm_bindgen(skip_typescript))]
#[derive(serde::Serialize, serde::Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "UPPERCASE")]
pub enum PortableType {
    ARRAY,
    NUMBER,
    STRING,
    NULL,
    OBJECT,
    BOOLEAN,
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[cfg_attr(feature = "wasm", wasm_bindgen(skip_typescript))]
#[derive(serde::Serialize, serde::Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct PortableValue {
    data: String,
    data_type: PortableType,
}

#[cfg(feature = "logic")]
#[pymethods]
impl PortableValue {
    #[new]
    pub fn create(data: &str, data_type: PortableType) -> PortableValue {
        PortableValue {
            data: data.to_string(),
            data_type,
        }
    }

    #[cfg(feature = "logic")]
    pub fn as_str(&self) -> PyResult<String> {
        if let Ok(v) = serde_json::from_str::<String>(&self.data) {
            return Ok(v);
        }
        Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unable to deserialize internal data: '{}'",
            self.data
        )))
    }

    #[cfg(feature = "logic")]
    pub fn as_int(&self) -> PyResult<i32> {
        if let Ok(v) = serde_json::from_str::<i32>(&self.data) {
            return Ok(v);
        }
        Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unable to deserialize internal data: '{}'",
            self.data
        )))
    }

    #[cfg(feature = "logic")]
    pub fn as_float(&self) -> PyResult<f32> {
        if let Ok(v) = serde_json::from_str::<f32>(&self.data) {
            return Ok(v);
        }
        Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unable to deserialize internal data: '{}'",
            self.data
        )))
    }

    #[pyo3(name = "json")]
    #[getter]
    pub fn py_data(&self) -> String {
        self.data.clone()
    }

    #[pyo3(name = "data_type")]
    #[getter]
    pub fn py_data_type(&self) -> PortableType {
        self.data_type.clone()
    }
}

impl PortableValue {
    pub fn new(data: &str, data_type: PortableType) -> PortableValue {
        PortableValue {
            data: data.to_string(),
            data_type,
        }
    }
    #[cfg(feature = "logic")]
    pub fn from<T: serde::Serialize>(value: T) -> Self {
        let data = serde_json::to_value(value).unwrap();
        match data {
            serde_json::Value::Array(a) => Self {
                data: stringify(&a),
                data_type: PortableType::ARRAY,
            },
            serde_json::Value::Number(a) => Self {
                data: stringify(&a),
                data_type: PortableType::NUMBER,
            },
            serde_json::Value::Null => Self {
                data: String::from("null"),
                data_type: PortableType::NULL,
            },
            serde_json::Value::Bool(a) => Self {
                data: stringify(&a),
                data_type: PortableType::BOOLEAN,
            },
            serde_json::Value::String(a) => Self {
                data: stringify(&a),
                data_type: PortableType::STRING,
            },
            serde_json::Value::Object(a) => Self {
                data: stringify(&a),
                data_type: PortableType::OBJECT,
            },
        }
    }

    pub fn from_str(sth: String) -> PortableValue {
        PortableValue {
            data: stringify(&sth),
            data_type: PortableType::STRING,
        }
    }
    pub fn from_vec<T: serde::Serialize + std::fmt::Debug>(sth: Vec<T>) -> PortableValue {
        PortableValue {
            data: stringify(&sth),
            data_type: PortableType::STRING,
        }
    }
    pub fn from_i32(sth: i32) -> PortableValue {
        PortableValue {
            data: stringify(&sth),
            data_type: PortableType::STRING,
        }
    }
    pub fn from_f32(sth: f32) -> PortableValue {
        PortableValue {
            data: stringify(&sth),
            data_type: PortableType::STRING,
        }
    }
    pub fn from_struct<T: serde::Serialize + std::fmt::Debug>(sth: T) -> PortableValue {
        PortableValue {
            data: stringify(&sth),
            data_type: PortableType::STRING,
        }
    }

    pub fn as_struct<'a, T: serde::de::DeserializeOwned>(sth: PortableValue) -> T {
        parse(&sth.data)
    }

    pub fn json(&self) -> String {
        self.data.clone()
    }

    pub fn data_type(&self) -> PortableType {
        self.data_type.clone()
    }
}

pub fn stringify<T>(sth: &T) -> String
where
    T: serde::Serialize + std::fmt::Debug,
{
    #[cfg(feature = "logic")]
    return logic::stringify(sth);
    #[cfg(not(feature = "logic"))]
    #[cfg(feature = "wasm")]
    return wasm::stringify(sth);
}

pub fn parse<'a, T>(data: &'a str) -> T
where
    T: serde::de::DeserializeOwned,
{
    #[cfg(feature = "logic")]
    return logic::parse(data);
    #[cfg(not(feature = "logic"))]
    #[cfg(feature = "wasm")]
    return wasm::parse(data);
}

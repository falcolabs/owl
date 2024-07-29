#[cfg(feature = "logic")]
use pyo3::prelude::*;

#[cfg(feature = "wasm")]
#[allow(dead_code)]
mod wasm {
    use serde_wasm_bindgen;

    pub fn stringify<T: serde::Serialize>(sth: &T) -> String {
        serde_wasm_bindgen::to_value(sth)
            .expect("JSON.stringify() error")
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

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(serde::Serialize, serde::Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "UPPERCASE")]
pub enum PortableValueType {
    ARRAY,
    NUMBER,
    STRING,
    NULL,
    OBJECT,
    BOOLEAN,
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(serde::Serialize, serde::Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct PortableValue {
    pub data: String,
    pub data_type: PortableValueType,
}

#[cfg(feature = "logic")]
#[pymethods]
impl PortableValue {
    #[new]
    pub fn new(data: &str, data_type: PortableValueType) -> PortableValue {
        PortableValue {
            data: data.to_string(),
            data_type,
        }
    }

    pub fn as_str(&self) -> PyResult<String> {
        if let Ok(v) = serde_json::from_str::<String>(&self.data) {
            return Ok(v);
        }
        Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unable to deserialize internal data: '{}'",
            self.data
        )))
    }

    pub fn as_int(&self) -> PyResult<i32> {
        if let Ok(v) = serde_json::from_str::<i32>(&self.data) {
            return Ok(v);
        }
        Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unable to deserialize internal data: '{}'",
            self.data
        )))
    }

    pub fn as_float(&self) -> PyResult<f32> {
        if let Ok(v) = serde_json::from_str::<f32>(&self.data) {
            return Ok(v);
        }
        Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unable to deserialize internal data: '{}'",
            self.data
        )))
    }

    pub fn data(&self) -> String {
        self.data.clone()
    }

    pub fn data_type(&self) -> PortableValueType {
        self.data_type.clone()
    }
}

impl PortableValue {
    #[cfg(feature = "logic")]
    pub fn from<T: serde::Serialize>(value: T) -> Self {
        let data = serde_json::to_value(value).unwrap();
        match data {
            serde_json::Value::Array(a) => Self {
                data: stringify(&a),
                data_type: PortableValueType::ARRAY,
            },
            serde_json::Value::Number(a) => Self {
                data: stringify(&a),
                data_type: PortableValueType::NUMBER,
            },
            serde_json::Value::Null => Self {
                data: String::from("null"),
                data_type: PortableValueType::NULL,
            },
            serde_json::Value::Bool(a) => Self {
                data: stringify(&a),
                data_type: PortableValueType::BOOLEAN,
            },
            serde_json::Value::String(a) => Self {
                data: stringify(&a),
                data_type: PortableValueType::STRING,
            },
            serde_json::Value::Object(a) => Self {
                data: stringify(&a),
                data_type: PortableValueType::OBJECT,
            },
        }
    }

    pub fn from_str(sth: String) -> PortableValue {
        PortableValue {
            data: stringify(&sth),
            data_type: PortableValueType::STRING,
        }
    }
    pub fn from_vec<T: serde::Serialize>(sth: Vec<T>) -> PortableValue {
        PortableValue {
            data: stringify(&sth),
            data_type: PortableValueType::STRING,
        }
    }
    pub fn from_i32(sth: i32) -> PortableValue {
        PortableValue {
            data: stringify(&sth),
            data_type: PortableValueType::STRING,
        }
    }
    pub fn from_f32(sth: f32) -> PortableValue {
        PortableValue {
            data: stringify(&sth),
            data_type: PortableValueType::STRING,
        }
    }
    pub fn from_struct<T: serde::Serialize>(sth: T) -> PortableValue {
        PortableValue {
            data: stringify(&sth),
            data_type: PortableValueType::STRING,
        }
    }

    pub fn as_struct<'a, T: serde::de::DeserializeOwned>(sth: PortableValue) -> T {
        parse(&sth.data)
    }
}

pub fn stringify<T>(sth: &T) -> String
where
    T: serde::Serialize,
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

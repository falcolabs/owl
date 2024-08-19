use crate::pyproperty;
#[cfg(feature = "net")]
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::fmt::Debug;

#[cfg_attr(feature = "logic", pyclass(subclass))]
#[derive(Debug)]
pub struct Part {
    #[cfg(feature = "logic")]
    #[pyo3(get)]
    pub implementation: Py<PyAny>,
    #[cfg(feature = "logic")]
    #[pyo3(get)]
    pub props: PartProperties,
    #[cfg(not(feature = "logic"))]
    pub props: PartProperties,
}

impl PartialEq for Part {
    fn eq(&self, other: &Self) -> bool {
        self.props == other.props
    }
}
impl Eq for Part {}

#[cfg(feature = "wasm")]
#[cfg(not(feature = "logic"))]
impl Clone for Part {
    fn clone(&self) -> Self {
        Self {
            props: self.props.clone(),
        }
    }
}

#[cfg(feature = "logic")]
impl Clone for Part {
    fn clone(&self) -> Self {
        unsafe {
            Self {
                implementation: self.implementation.clone_ref(Python::assume_gil_acquired()),
                props: self.props.clone(),
            }
        }
    }
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
pub struct PartProperties {
    pub name: String,
}
pyproperty!(PartProperties:name -> String);

#[cfg(feature = "logic")]
#[pymethods]
impl Part {
    #[new]
    pub fn new(wrapped: Py<PyAny>, name: String) -> Self {
        Part {
            implementation: wrapped,
            props: PartProperties { name },
        }
    }
}

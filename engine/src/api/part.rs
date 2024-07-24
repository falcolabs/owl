#[cfg(feature = "net")]
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::fmt::Debug;

// #[cfg_attr(feature = "logic", pyclass)]
// #[derive(Serialize, Deserialize, Clone, Debug)]
// pub struct PartProperties {
//     pub name: String,
// }

// #[cfg(feature = "logic")]
// /// Represents the logic of a particular part of a show.
// pub trait Part: PartClone + Debug + Sync + Send + crate::api::Resource {
//     /// Called once per tick, this function contains the logic of the part.
//     fn on_update(&mut self, show: PyRefMut<Show>) -> Status;

//     fn get_properties(&self) -> PartProperties;

//     #[cfg(feature = "net")]
//     fn on_request(
//         &mut self,
//         show: PyRefMut<Show>,
//         packet: Packet,
//         handle: IOHandle,
//         addr: std::net::SocketAddr,
//         message: String,
//     ) -> BoxFuture<'static, ()>;
// }
// #[cfg(feature = "logic")]
// pub trait MessageHandler {}

// #[cfg(feature = "logic")]
// pub trait PartClone {
//     fn clone_box(&self) -> Box<dyn Part>;
// }

// #[cfg(feature = "logic")]
// impl<T> PartClone for T
// where
//     T: 'static + Part + Clone,
// {
//     fn clone_box(&self) -> Box<dyn Part> {
//         Box::new(self.clone())
//     }
// }

// #[cfg(feature = "logic")]
// impl Clone for Box<dyn Part> {
//     fn clone(&self) -> Box<dyn Part> {
//         self.clone_box()
//     }
// }
#[cfg_attr(feature = "logic", pyclass(module = "engine", subclass))]
#[derive(Debug, Clone)]
pub struct Part {
    #[cfg(feature = "logic")]
    #[pyo3(get)]
    pub implementation: PyObject,
    #[cfg(feature = "logic")]
    #[pyo3(get)]
    pub props: PartProperties,
    #[cfg(not(feature = "logic"))]
    pub props: PartProperties,
}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
pub struct PartProperties {
    pub name: String,
}

#[cfg(feature = "logic")]
impl PartialEq for Part {
    fn eq(&self, other: &Part) -> bool {
        self.props == other.props
    }
}

#[cfg(feature = "logic")]
#[pymethods]
impl Part {
    #[new]
    pub fn new(wrapped: PyObject, name: String) -> Self {
        Part {
            implementation: wrapped,
            props: PartProperties { name },
        }
    }
}

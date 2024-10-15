pub use crate::api::player::Player;
use crate::net::wspy::IOHandle;
use pyo3::prelude::*;

#[pymethods]
#[allow(unused)]
impl Player {
    #[new]
    pub fn create(identifier: String, name: String, score: i32) -> Self {
        Player::new(identifier, name, score)
    }

    #[getter(handle)]
    pub fn handle(&self) -> PyResult<crate::net::wspy::IOHandle> {
        match &self.handle {
            Some(a) => Ok(a.clone()),
            None => Err(pyo3::exceptions::PyValueError::new_err(format!(
                "Handle for player {}: '{}' is unset.",
                self.identifier, self.name
            ))),
        }
    }

    #[setter(handle)]
    pub fn set_handle(&mut self, handle: IOHandle) {
        self.handle = Some(handle);
    }

    pub fn add_score(&mut self, additional_score: i32) -> i32 {
        self.score += additional_score;
        self.score
    }

    pub fn pack(&self) -> String {
        serde_json::to_string(self).unwrap()
    }

    #[staticmethod]
    pub fn from_json(data: String) -> Self {
        serde_json::from_str(&data).unwrap()
    }
}

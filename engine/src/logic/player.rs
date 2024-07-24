pub use crate::api::player::Player;
use pyo3::prelude::*;

#[pymethods]
#[allow(unused)]
impl Player {
    #[new]
    pub fn new(identifier: String, name: String, score: i32) -> Self {
        Player {
            identifier,
            name,
            score,
        }
    }

    fn add_score(&mut self, additional_score: i32) -> i32 {
        self.score += additional_score;
        self.score
    }
}

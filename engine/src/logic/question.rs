pub use crate::api::{Question, QuestionBank};
use crate::logging;
use pyo3::{exceptions::PyIndexError, prelude::*};
use rand::{seq::SliceRandom, thread_rng};
use std::fs;

#[pymethods]
impl Question {
    #[new]
    pub fn new(
        prompt: String,
        key: String,
        score: i32,
        choices: Vec<String>,
        score_false: i32,
        explaination: String,
    ) -> Question {
        Question {
            prompt,
            key,
            score,
            choices,
            score_false,
            explaination,
        }
    }
}

impl Default for QuestionBank {
    fn default() -> Self {
        Self::new()
    }
}

#[pymethods]
impl QuestionBank {
    #[new]
    pub fn new() -> QuestionBank {
        QuestionBank {
            question_storage: Vec::new(),
        }
    }

    /// Load questions from a JSON file and stores it.
    /// It should have the following structure:
    /// ```json
    /// [
    ///   {
    ///     "prompt": "What is one plus one?",
    ///     "key": "Two",
    ///     "score": 100,
    ///     // Optional properties
    ///     "choices": ["One", "Two", "Three", "One Million Five Hundred and Fifty Two Thousand Seven Hundred and Three"],
    ///     "score_false": -5,
    ///     "explaination": "bruh"
    ///   },
    ///   ...
    /// ]
    /// ```
    pub fn load(&mut self, filepath: &str) {
        self.question_storage = serde_json::from_str(
            fs::read_to_string(filepath)
                .unwrap_or_else(|_| panic!("{}", logging::error_str("Unable to read file")))
                .as_str(),
        )
        .unwrap_or_else(|_| panic!("{}", logging::error_str("Invalid JSON structure.")));
    }

    /// Gets the question with the specified ID.
    /// Will panic if no questions with the specified ID exists.
    pub fn get_question(&self, question_id: usize) -> PyResult<Question> {
        match self.question_storage.get(question_id) {
            Some(q) => Ok(q.clone()),
            None => Python::with_gil(|_| {
                Err(PyIndexError::new_err(format!(
                    "Cannt read question with id {}.",
                    question_id
                )))
            })
            .expect("Cannot raise IndexError"),
        }
    }

    /// Gets a random question.
    /// Panics if there are no questions in the bank.
    pub fn random_question(&self) -> Question {
        if self.question_storage.is_empty() {
            panic!(
                "{}",
                logging::error_str("Cannot get random question in an empty question bank.")
            )
        }
        let mut rng = thread_rng();
        self.question_storage
            .choose(&mut rng)
            .unwrap_or_else(|| {
                panic!(
                    "{}",
                    logging::error_str("Cannot choose random question.").as_str()
                )
            })
            .clone()
    }

    /// Gets a specified number of unique random questions.
    /// Panics if there are no questions in the bank.
    pub fn random_n_questions(&self, n: usize) -> Vec<Question> {
        if self.question_storage.is_empty() {
            panic!(
                "{}",
                logging::error_str("Cannot get random n question in an empty question bank.")
            )
        }
        let mut rng = thread_rng();
        let mut output: Vec<Question> = Vec::new();
        self.question_storage
            .choose_multiple(&mut rng, n)
            .for_each(|q| output.push(q.clone()));

        output
    }
}

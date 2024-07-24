#[allow(unused)]
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Clone, Debug)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct Question {
    pub prompt: String,
    pub key: String,
    pub score: i32,
    pub choices: Option<Vec<String>>,
    pub score_false: Option<i32>,
    pub explaination: Option<String>,
}

impl crate::api::Resource for Question {}

#[cfg_attr(feature = "logic", pyclass(module = "engine"))]
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct QuestionBank {
    pub question_storage: Vec<Question>,
}

impl crate::api::Resource for QuestionBank {}

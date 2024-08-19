use crate::pyproperty;
#[allow(unused)]
#[cfg(feature = "logic")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[cfg_attr(feature = "logic", pyclass)]
#[derive(Serialize, Deserialize, Clone, Debug, Eq, PartialEq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct Question {
    pub prompt: String,
    pub key: String,
    pub score: i32,
    pub choices: Vec<String>,
    pub score_false: i32,
    pub explaination: String,
}
pyproperty!( Question:prompt       -> String      );
pyproperty!( Question:key          -> String      );
pyproperty!( Question:score        -> i32         );
pyproperty!( Question:choices      -> Vec<String> );
pyproperty!( Question:score_false  -> i32         );
pyproperty!( Question:explaination -> String      );

impl crate::api::Resource for Question {}

#[cfg_attr(feature = "logic", pyclass)]
#[derive(Serialize, Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct QuestionBank {
    pub question_storage: Vec<Question>,
}
pyproperty!(QuestionBank:question_storage -> Vec<Question>);

impl crate::api::Resource for QuestionBank {}

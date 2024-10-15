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
    #[serde(default)]
    pub media: Option<MediaContent>,
    pub key: String,
    pub score: i32,
    // TODO - more specific unit like thinkSeconds rather than
    // just time.
    pub time: i32,
    #[serde(default)]
    pub choices: Vec<String>,
    #[serde(default)]
    pub score_false: i32,
    #[serde(default)]
    pub explaination: String,
}
pyproperty!( Question:prompt       -> String               );
pyproperty!( Question:media        -> Option<MediaContent> );
pyproperty!( Question:key          -> String               );
pyproperty!( Question:score        -> i32                  );
pyproperty!( Question:time         -> i32                  );
pyproperty!( Question:choices      -> Vec<String>          );
pyproperty!( Question:score_false  -> i32                  );
pyproperty!( Question:explaination -> String               );

#[cfg_attr(feature = "logic", pyclass)]
#[derive(Serialize, Deserialize, Clone, Debug, Eq, PartialEq, Default)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct MediaContent {
    pub media_type: String,
    pub uri: String,
}

#[cfg(feature = "logic")]
#[pymethods]
impl MediaContent {
    #[new]
    pub fn new(media_type: String, uri: String) -> Self {
        Self { media_type, uri }
    }

    pub fn pack(&self) -> String {
        serde_json::to_string(self).unwrap()
    }
}

pyproperty!( MediaContent:media_type:set_media_type  -> String );
pyproperty!( MediaContent:uri:set_uri                -> String );

impl crate::api::Resource for Question {}

#[cfg_attr(feature = "logic", pyclass)]
#[derive(Serialize, Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct QuestionBank {
    pub question_storage: Vec<Question>,
}
pyproperty!(QuestionBank:question_storage -> Vec<Question>);

impl crate::api::Resource for QuestionBank {}

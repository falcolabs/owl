use core::panic;

use crate::logging::Color;
use chrono::prelude::Local;
#[cfg(feature = "logic")]
use pyo3::prelude::*;

#[cfg_attr(feature = "logic", pyclass(eq, eq_int))]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Level {
    DEBUG,
    SUCCESS,
    INFO,
    WARNING,
    ERROR,
}

#[cfg_attr(feature = "logic", pymethods)]
impl Level {
    pub fn get_color(&self) -> Color {
        match *self {
            Level::DEBUG => Color::CYAN,
            Level::SUCCESS => Color::GREEN,
            Level::INFO => Color::WHITE,
            Level::WARNING => Color::YELLOW,
            Level::ERROR => Color::RED,
        }
    }

    pub fn get_prio(&self) -> i32 {
        match *self {
            Level::DEBUG => -2,
            Level::SUCCESS => -1,
            Level::INFO => 0,
            Level::WARNING => 1,
            Level::ERROR => 2,
        }
    }

    pub fn get_name(&self) -> &str {
        match *self {
            Level::DEBUG => "DEBUG",
            Level::SUCCESS => "SUCCESS",
            Level::INFO => "INFO",
            Level::WARNING => "WARNING",
            Level::ERROR => "ERROR",
        }
    }
}

#[allow(static_mut_refs)]
static mut MINIMUM_LEVEL: Level = Level::INFO;

#[cfg_attr(feature = "logic", pyfunction)]
pub fn set_log_level(min_level: Level) {
    unsafe {
        MINIMUM_LEVEL = min_level;
    }
}

pub fn log<StringLike: AsRef<str>>(level: Level, content: StringLike) {
    // pyo3::Python::with_gil(|py| {
    //     py.run_bound(
    //         // &command,
    //         format!(
    //             r#"import sys; sys.stdout.write('{}')"#,
    //             log_str(level, content)
    //         )
    //         .as_str(),
    //         // format!("print(\"{}\")", ).as_str(),
    //         Option::None,
    //         Option::None,
    //     )
    //     .unwrap();
    // })
    print!("{}", log_str(level, content));
}

pub fn log_str<StringLike: AsRef<str>>(level: Level, content: StringLike) -> String {
    if level.get_prio() < unsafe { MINIMUM_LEVEL.get_prio() } {
        return String::new();
    }
    let time = Local::now();
    // TODO - chick-like log formatting
    // TODO - force log clients to specify name using a Logger instance.
    let result = format!(
        "{}[{} {}] {}{}\n",
        level.get_color().as_str(),
        time.format("%H:%M:%S"),
        level.get_name(),
        content.as_ref(),
        Color::RESET.as_str()
    );
    result
}

#[cfg_attr(feature = "logic", pyfunction(name = "log_debug"))]
pub fn py_debug(content: String) {
    debug(content);
}

#[cfg_attr(feature = "logic", pyfunction(name = "log_success"))]
pub fn py_success(content: String) {
    success(content);
}

#[cfg_attr(feature = "logic", pyfunction(name = "log_info"))]
pub fn py_info(content: String) {
    info(content);
}

#[cfg_attr(feature = "logic", pyfunction(name = "log_warning"))]
pub fn py_warning(content: String) {
    warning(content);
}

#[cfg_attr(feature = "logic", pyfunction(name = "log_error"))]
pub fn py_error(content: String) {
    error(content);
}

pub fn debug<StringLike: AsRef<str>>(content: StringLike) {
    log(Level::DEBUG, content.as_ref());
}

pub fn success<StringLike: AsRef<str>>(content: StringLike) {
    log(Level::SUCCESS, content.as_ref());
}

pub fn info<StringLike: AsRef<str>>(content: StringLike) {
    log(Level::INFO, content.as_ref());
}

pub fn warning<StringLike: AsRef<str>>(content: StringLike) {
    log(Level::WARNING, content.as_ref());
}
pub fn error<StringLike: AsRef<str>>(content: StringLike) {
    log(Level::ERROR, content.as_ref());
}

pub fn debug_str<StringLike: AsRef<str>>(content: StringLike) -> String {
    log_str(Level::DEBUG, content.as_ref())
}

pub fn success_str<StringLike: AsRef<str>>(content: StringLike) -> String {
    log_str(Level::SUCCESS, content.as_ref())
}

pub fn info_str<StringLike: AsRef<str>>(content: StringLike) -> String {
    log_str(Level::INFO, content.as_ref())
}

pub fn warning_str<StringLike: AsRef<str>>(content: StringLike) -> String {
    log_str(Level::WARNING, content.as_ref())
}
pub fn error_str<StringLike: AsRef<str>>(content: StringLike) -> String {
    log_str(Level::ERROR, content.as_ref())
}

pub fn debug_panic<StringLike: AsRef<str>>(content: StringLike) {
    panic!("{}", log_str(Level::DEBUG, content.as_ref()))
}

pub fn success_panic<StringLike: AsRef<str>>(content: StringLike) {
    panic!("{}", log_str(Level::SUCCESS, content.as_ref()))
}

pub fn info_panic<StringLike: AsRef<str>>(content: StringLike) {
    panic!("{}", log_str(Level::INFO, content.as_ref()))
}

pub fn warning_panic<StringLike: AsRef<str>>(content: StringLike) {
    panic!("{}", log_str(Level::WARNING, content.as_ref()))
}
pub fn error_panic<StringLike: AsRef<str>>(content: StringLike) {
    panic!("{}", log_str(Level::ERROR, content.as_ref()))
}

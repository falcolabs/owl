#[cfg(feature = "logic")]
use pyo3::prelude::*;

#[allow(dead_code, non_camel_case_types)]
#[cfg_attr(feature = "logic", pyclass(eq, eq_int))]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Color {
    BLACK,
    RED,
    GREEN,
    YELLOW,
    BLUE,
    MAGENTA,
    CYAN,
    WHITE,
    BRIGHT_BLACK,
    GRAY,
    GREY,
    BRIGHT_RED,
    BRIGHT_GREEN,
    BRIGHT_YELLOW,
    BRIGHT_BLUE,
    BRIGHT_MAGENTA,
    BRIGHT_CYAN,
    BRIGHT_WHITE,
    RESET,
    BOLD,
    UNDERLINE,
    REVERSED,
    BLANK,
}

#[cfg_attr(feature = "logic", pyfunction)]
pub fn to_color(code: String) -> Color {
    match code.as_str() {
        "0" => Color::BLACK,
        "1" => Color::BLUE,
        "2" => Color::GREEN,
        "3" => Color::CYAN,
        "4" => Color::RED,
        "5" => Color::MAGENTA,
        "6" => Color::YELLOW,
        "7" => Color::GRAY,
        "8" => Color::GRAY,
        "9" => Color::BLUE,
        "a" => Color::BRIGHT_GREEN,
        "b" => Color::BRIGHT_CYAN,
        "c" => Color::BRIGHT_RED,
        "d" => Color::BRIGHT_MAGENTA,
        "e" => Color::BRIGHT_YELLOW,
        "f" => Color::WHITE,
        "r" => Color::RESET,
        "l" => Color::BOLD,
        "n" => Color::UNDERLINE,
        _ => Color::BLANK,
    }
}

#[cfg_attr(feature = "logic", pymethods)]
impl Color {
    pub fn as_str(&self) -> &str {
        match *self {
            Color::BLACK => "\x1b[30m",
            Color::RED => "\x1b[31m",
            Color::GREEN => "\x1b[32m",
            Color::YELLOW => "\x1b[33m",
            Color::BLUE => "\x1b[34m",
            Color::MAGENTA => "\x1b[35m",
            Color::CYAN => "\x1b[36m",
            Color::WHITE => "\x1b[37m",
            Color::BRIGHT_BLACK => "\x1b[30;1m",
            Color::GRAY => "\x1b[30;1m",
            Color::GREY => "\x1b[30;1m",
            Color::BRIGHT_RED => "\x1b[31;1m",
            Color::BRIGHT_GREEN => "\x1b[32;1m",
            Color::BRIGHT_YELLOW => "\x1b[33;1m",
            Color::BRIGHT_BLUE => "\x1b[34;1m",
            Color::BRIGHT_MAGENTA => "\x1b[35;1m",
            Color::BRIGHT_CYAN => "\x1b[36;1m",
            Color::BRIGHT_WHITE => "\x1b[37;1m",
            Color::RESET => "\x1b[0m",
            Color::BOLD => "\x1b[1m",
            Color::UNDERLINE => "\x1b[4m",
            Color::REVERSED => "\x1b[7m",
            Color::BLANK => "",
        }
    }
}

#[cfg_attr(feature = "logic", pyfunction)]
pub fn mccolor(text: &str) -> String {
    mccolor_esc(text, "&")
}

#[cfg_attr(feature = "logic", pyfunction)]
pub fn mccolor_esc(text: &str, esc_char: &str) -> String {
    let mut output: String = String::new();
    let mut is_escape_seq: bool = false;
    for c in text.chars() {
        if c.to_string() == esc_char {
            is_escape_seq = true;
            continue;
        }

        if is_escape_seq {
            output.push_str(to_color(c.to_string()).as_str());
            is_escape_seq = false;
        } else {
            output.push(c);
        }
    }

    output
}

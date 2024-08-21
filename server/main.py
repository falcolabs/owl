import engine
import logic.auth
import logic.khoidong

import penguin
import config


def main():
    qbank = engine.QuestionBank()
    qbank.load("../assets/question_khoidong.json")
    config.load("../config.json")
    penguin.set_error_hook()

    if config.config().debug:
        engine.set_log_level(engine.Level.DEBUG)

    show = penguin.ShowBootstrap(
        "Đáy xã hội 2",
        [engine.Part(logic.khoidong.KhoiDong(), "khoidong")],
        [engine.Player(c.username, c.fullName, 0) for c in config.config().credentials],
        60,
        qbank,
    )
    penguin.SHOW = show

    show.start(
        "localhost:6942",
        "dist",
        "static",
    )


if __name__ == "__main__":
    main()

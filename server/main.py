import engine
import logic.auth
import logic.khoidong
import logic.vcnv

import penguin
import config


def main():
    qbank = engine.QuestionBank()
    qbank.load("../assets/question_template.json")
    config.load("../config.json")
    penguin.set_error_hook()

    if config.config().debug:
        engine.set_log_level(engine.Level.DEBUG)

    show = penguin.ShowBootstrap(
        "Đáy xã hội 2",
        [
            engine.Part(logic.vcnv.VCNV(), "vcnv"),
            engine.Part(logic.khoidong.KhoiDong(), "khoidong"),
        ],
        [engine.Player(c.username, c.fullName, 0) for c in config.config().credentials],
        config.config().tickSpeed,
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

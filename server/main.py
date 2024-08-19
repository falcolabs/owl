import engine
import logic.auth
import logic.khoidong
import utils
import config

qbank = engine.QuestionBank()
qbank.load("../assets/question_khoidong.json")
config.load("../config.json")
if config.config().debug:
    engine.set_log_level(engine.Level.DEBUG)

show = utils.ShowBootstrap(
    "Đáy xã hội 2",
    [engine.Part(logic.khoidong.KhoiDong(), "khoidong")],
    [engine.Player(c.username, c.fullName, 0) for c in config.config().credentials],
    60,
    qbank,
)

show.start(
    "localhost:6942",
    "dist",
    "static",
)

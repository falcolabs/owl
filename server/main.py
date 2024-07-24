import engine
import logic.auth
import pengin

qbank = engine.QuestionBank()
qbank.load("../assets/question_test.json")

show = pengin.Show(
    "Đáy xã hội 2",
    [engine.Part(logic.auth.Auth(), "auth")],
    [
        engine.Player("mrbeast69", "DONALDSON, Jimmy", 0),
        engine.Player("lequydon", "QUY DON, Le", 0),
        engine.Player("joe", "JOE, Biden", 0),
        engine.Player("trump", "DONALD, John Pump", 0),
    ],
    60,
    qbank,
)

show.start(
    "localhost:6942",
    "dist",
    "static",
)

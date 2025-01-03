import datetime
import os

if not os.path.exists("../logs"):
    os.mkdir("../logs")

# filename = f"game_{datetime.datetime.now().isoformat()}.log"
filename = f"latest.log"


def log(ident: str, message: str):
    print(ident, message)
    with open(f"../logs/{filename}", "a", encoding="utf8") as f:
        f.write(
            f"{datetime.datetime.now().strftime("%H:%M:%S.%f")}\t{ident}\t{message}\n"
        )


log("engine", f"GAME START")

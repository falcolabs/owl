import json
import os

import pylightxl  # type: ignore[reportMissingTypeStubs]
from pylightxl.pylightxl import Worksheet  # type: ignore[reportMissingTypeStubs]


def ddx_loader(db: Worksheet):
    output = []
    for i in range(6, 42):
        output.append(
            {
                "prompt": db.address(f"D{i}"),
                "key": db.address(f"E{i}"),
                "score": int(db.address(f"F{i}")),
                "time": int(db.address(f"H{i}")),
                "media": None,
                "choices": [],
                "scoreFalse": int(db.address(f"G{i}")),
                "explaination": db.address(f"I{i}"),
            }
        )
    output += [
        *[
            {
                "prompt": db.address(f"D{i}"),
                "key": str(db.address(f"E{i}")).upper().replace(" ", ""),
                "score": int(db.address(f"F{i}")),
                "time": int(db.address(f"H{i}")),
                "media": None,
                "choices": [],
                "scoreFalse": int(db.address(f"G{i}")),
                "explaination": db.address(f"I{i}"),
            }
            for i in range(43, 48)
        ],
        {
            "prompt": "Hãy nhập đáp án cho chướng ngại vật",
            "key": str(db.address(f"E42")).upper().replace(" ", ""),
            "score": 0,
            "time": 15,
            "media": None,
            "choices": [],
            "scoreFalse": 0,
            "explaination": "",
        },
    ]
    for i in range(48, 79):
        output.append(
            {
                "prompt": db.address(f"D{i}"),
                "key": db.address(f"E{i}"),
                "score": int(db.address(f"F{i}")),
                "time": int(db.address(f"H{i}")),
                "media": None,
                "choices": [],
                "scoreFalse": int(db.address(f"G{i}")),
                "explaination": db.address(f"I{i}"),
            }
        )
    with open(
        os.path.join("assets", "question_official.json"), "w", encoding="utf8"
    ) as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    with open("config.json", "w", encoding="utf8") as f:
        json.dump(
            {
                "listenOn": {"host": db.address("M12"), "port": int(db.address("M13"))},
                "devServer": {
                    "host": db.address("M14"),
                    "port": int(db.address("M15")),
                },
                "serveDir": db.address("M16"),
                "staticDir": db.address("M17"),
                "checkRPCTypes": db.address("M18"),
                "debug": db.address("M19"),
                "tickSpeed": int(db.address("M20")),
                "credentials": [
                    {
                        "fullName": db.address("M7"),
                        "username": db.address("N7"),
                        "accessKey": db.address("O7"),
                    },
                    {
                        "fullName": db.address("M8"),
                        "username": db.address("N8"),
                        "accessKey": db.address("O8"),
                    },
                    {
                        "fullName": db.address("M9"),
                        "username": db.address("N9"),
                        "accessKey": db.address("O9"),
                    },
                    {
                        "fullName": db.address("M10"),
                        "username": db.address("N10"),
                        "accessKey": db.address("O10"),
                    },
                ],
                "game": {
                    "vcnv": {
                        "keyLength": len(
                            str(db.address("E42")).upper().replace(" ", "")
                        ),
                        "qualityPercentage": int(db.address("M22")),
                        "keyResolution": {
                            "width": int(db.address("M23")),
                            "height": int(db.address("M24")),
                        },
                    }
                },
            },
            f,
            ensure_ascii=False,
            indent=4,
        )


def olympus_loader(db: Worksheet):
    output = []
    p1, p2, p3, p4 = [], [], [], []
    for i in range(8, 14):
        p1.append(
            {
                "prompt": db.address(f"B{i}"),
                "key": db.address(f"C{i}"),
                "score": 10,
                "time": 3,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
        p2.append(
            {
                "prompt": db.address(f"D{i}"),
                "key": db.address(f"E{i}"),
                "score": 10,
                "time": 3,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
        p3.append(
            {
                "prompt": db.address(f"F{i}"),
                "key": db.address(f"G{i}"),
                "score": 10,
                "time": 3,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
        p4.append(
            {
                "prompt": db.address(f"H{i}"),
                "key": db.address(f"I{i}"),
                "score": 10,
                "time": 3,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
    output += [*p1, *p2, *p3, *p4]

    for i in range(73, 85):
        output.append(
            {
                "prompt": db.address(f"B{i}"),
                "key": db.address(f"C{i}"),
                "score": 10,
                "time": 3,
                "media": None,
                "choices": [],
                "scoreFalse": -5,
                "explaination": "",
            }
        )

    output += [
        *[
            {
                "prompt": db.address(f"B{i}"),
                "key": str(db.address(f"C{i}")).upper().replace(" ", ""),
                "score": 10,
                "time": 15,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
            for i in range(20, 25)
        ],
        {
            "prompt": "Hãy nhập đáp án cho chướng ngại vật",
            "key": str(db.address(f"B18")).upper().replace(" ", ""),
            "score": 0,
            "time": 15,
            "media": None,
            "choices": [],
            "scoreFalse": 0,
            "explaination": "",
        },
    ]
    output += [
        {
            "prompt": db.address(f"B30"),
            "key": db.address(f"C30"),
            "score": 0,
            "time": 10,
            "media": None,
            "choices": [],
            "scoreFalse": 0,
            "explaination": "",
        },
        {
            "prompt": db.address(f"B31"),
            "key": db.address(f"C31"),
            "score": 0,
            "time": 20,
            "media": None,
            "choices": [],
            "scoreFalse": 0,
            "explaination": "",
        },
        {
            "prompt": db.address(f"B32"),
            "key": db.address(f"C32"),
            "score": 0,
            "time": 30,
            "media": None,
            "choices": [],
            "scoreFalse": 0,
            "explaination": "",
        },
        {
            "prompt": db.address(f"B33"),
            "key": db.address(f"C33"),
            "score": 0,
            "time": 40,
            "media": None,
            "choices": [],
            "scoreFalse": 0,
            "explaination": "",
        },
    ]
    p1, p2, p3, p4 = [], [], [], []
    for i in range(42, 45):
        p1.append(
            {
                "prompt": db.address(f"B{i}"),
                "key": db.address(f"C{i}"),
                "score": 20,
                "time": 15,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
        p2.append(
            {
                "prompt": db.address(f"D{i}"),
                "key": db.address(f"E{i}"),
                "score": 20,
                "time": 15,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
        p3.append(
            {
                "prompt": db.address(f"F{i}"),
                "key": db.address(f"G{i}"),
                "score": 20,
                "time": 15,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
        p4.append(
            {
                "prompt": db.address(f"H{i}"),
                "key": db.address(f"I{i}"),
                "score": 20,
                "time": 15,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
    for i in range(45, 48):
        p1.append(
            {
                "prompt": db.address(f"B{i}"),
                "key": db.address(f"C{i}"),
                "score": 30,
                "time": 20,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
        p2.append(
            {
                "prompt": db.address(f"D{i}"),
                "key": db.address(f"E{i}"),
                "score": 30,
                "time": 20,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
        p3.append(
            {
                "prompt": db.address(f"F{i}"),
                "key": db.address(f"G{i}"),
                "score": 30,
                "time": 20,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
        p4.append(
            {
                "prompt": db.address(f"H{i}"),
                "key": db.address(f"I{i}"),
                "score": 30,
                "time": 20,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )
    output += [*p1, *p2, *p3, *p4]
    # Olympus supports more than 3, but rules state only 3 would be available.
    # See https://duong-len-dinh-olympia.fandom.com/vi/wiki/Lu%E1%BA%ADt_ch%C6%A1i#24,_25.
    for i in range(53, 56):
        output.append(
            {
                "prompt": db.address(f"B{i}"),
                "key": db.address(f"C{i}"),
                "score": 10,
                "time": 15,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )

    with open(
        os.path.join("assets", "question_official.json"), "w", encoding="utf8"
    ) as f:
        json.dump(output, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print("Syncing questions...")
    f = pylightxl.readxl("config.xlsx")
    db = f.ws(f.ws_names[0])
    if db.address("A1") == "ĐƯỜNG ĐUA XANH - CÀI ĐẶT CHƯƠNG TRÌNH":
        print("DDX configuration file detected.")
        ddx_loader(db)
    elif db.address("A3") == "Tên trận/giải đấu (nhập vào ô bên phải) [BẮT BUỘC]":
        print("Olympus configuration file detected.")
        olympus_loader(db)
    else:
        print("Invalid file formet. Only Olympus Online and DDX are supported.")
        exit(0)
    print("Complete.")

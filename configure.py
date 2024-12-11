import json
import os
import pathlib
import tqdm
import requests
import pylightxl  # type: ignore[reportMissingTypeStubs]
from pylightxl.pylightxl import Worksheet  # type: ignore[reportMissingTypeStubs]

session = requests.Session()


def download_ggdrive(url: str, save_as: str) -> str | None:
    download_url = "https://docs.google.com/uc?export=download&confirm=1"
    if url == "":
        return None
    response = session.get(download_url, params={"id": url[32:65]}, stream=True)

    with tqdm.tqdm(
        total=int(response.headers.get("content-length", 0)),
        unit="B",
        unit_scale=True,
        ascii="░▒█",
        desc=pathlib.PurePath(save_as).name.ljust(7),
    ) as progress_bar:
        with open(save_as, "wb") as file:
            for data in response.iter_content(1024):
                progress_bar.update(len(data))
                file.write(data)
    return save_as


def ddx_loaderv02(db: Worksheet):
    output = []
    for i in range(6, 42):
        output.append(
            {
                "prompt": db.address(f"D{i}"),
                "key": str(db.address(f"E{i}")),
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
    download_ggdrive(str(db.address(f"D42")), os.path.join("assets", "vcnv", "key.png"))
    for i in range(49, 53):
        output.append(
            {
                "prompt": db.address(f"D{i}"),
                "key": str(db.address(f"E{i}")),
                "score": int(db.address(f"F{i}")),
                "time": int(db.address(f"H{i}")),
                "media": None,
                "choices": [],
                "scoreFalse": int(db.address(f"G{i}")),
                "explaination": db.address(f"I{i}"),
            }
        )
    for i in range(54, 81):
        output.append(
            {
                "prompt": db.address(f"D{i}"),
                "key": str(db.address(f"E{i}")),
                "score": int(db.address(f"F{i}")),
                "time": int(db.address(f"H{i}")),
                "media": None,
                "choices": [],
                "scoreFalse": int(db.address(f"G{i}")),
                "explaination": db.address(f"I{i}"),
            }
        )
    output[42]["media"] = {
        "mediaType": "image",
        "uri": "/tangtoc/q1.png",
    }
    output[43]["media"] = {
        "mediaType": "image",
        "uri": "/tangtoc/q2.png",
    }
    output[44]["media"] = {
        "mediaType": "image",
        "uri": "/tangtoc/q3.png",
    }
    output[45]["media"] = {
        "mediaType": "video",
        "uri": "/tangtoc/q4.mp4",
    }
    download_ggdrive(
        str(db.address("C49")), os.path.join("assets/public/tangtoc/q1.png")
    )
    download_ggdrive(
        str(db.address("C50")), os.path.join("assets/public/tangtoc/q2.png")
    )
    download_ggdrive(
        str(db.address("C51")), os.path.join("assets/public/tangtoc/q3.png")
    )
    download_ggdrive(
        str(db.address("C52")), os.path.join("assets/public/tangtoc/q4.mp4")
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
                "gameAssets": [
                    "/tangtoc/q1.png",
                    "/tangtoc/q2.png",
                    "/tangtoc/q3.png",
                    "/tangtoc/q4.mp4",
                ],
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
    print("Đã viết config.json")


def ddx_loaderv01(db: Worksheet):
    output = []
    for i in range(6, 42):
        output.append(
            {
                "prompt": db.address(f"D{i}"),
                "key": str(db.address(f"E{i}")),
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
                "key": str(db.address(f"E{i}")),
                "score": int(db.address(f"F{i}")),
                "time": int(db.address(f"H{i}")),
                "media": None,
                "choices": [],
                "scoreFalse": int(db.address(f"G{i}")),
                "explaination": db.address(f"I{i}"),
            }
        )
    output[42]["media"] = {
        "mediaType": "image",
        "uri": "/tangtoc/q1.png",
    }
    output[43]["media"] = {
        "mediaType": "image",
        "uri": "/tangtoc/q2.png",
    }
    output[44]["media"] = {
        "mediaType": "image",
        "uri": "/tangtoc/q3.png",
    }
    output[45]["media"] = {
        "mediaType": "video",
        "uri": "/tangtoc/q4.mp4",
    }
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
                "gameAssets": [
                    "/tangtoc/q1.png",
                    "/tangtoc/q2.png",
                    "/tangtoc/q3.png",
                    "/tangtoc/q4.mp4",
                ],
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
    print("Đã viết config.json")


def olympus_loader(db: Worksheet):
    output = []
    p1, p2, p3, p4 = [], [], [], []
    for i in range(8, 14):
        p1.append(
            {
                "prompt": db.address(f"B{i}"),
                "key": str(db.address(f"C{i}")),
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
                "key": str(db.address(f"E{i}")),
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
                "key": str(db.address(f"G{i}")),
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
                "key": str(db.address(f"I{i}")),
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
                "key": str(db.address(f"C{i}")),
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
            "key": str(db.address(f"C30")),
            "score": 0,
            "time": 10,
            "media": None,
            "choices": [],
            "scoreFalse": 0,
            "explaination": "",
        },
        {
            "prompt": db.address(f"B31"),
            "key": str(db.address(f"C31")),
            "score": 0,
            "time": 20,
            "media": None,
            "choices": [],
            "scoreFalse": 0,
            "explaination": "",
        },
        {
            "prompt": db.address(f"B32"),
            "key": str(db.address(f"C32")),
            "score": 0,
            "time": 30,
            "media": None,
            "choices": [],
            "scoreFalse": 0,
            "explaination": "",
        },
        {
            "prompt": db.address(f"B33"),
            "key": str(db.address(f"C33")),
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
                "key": str(db.address(f"C{i}")),
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
                "key": str(db.address(f"E{i}")),
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
                "key": str(db.address(f"G{i}")),
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
                "key": str(db.address(f"I{i}")),
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
                "key": str(db.address(f"C{i}")),
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
                "key": str(db.address(f"E{i}")),
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
                "key": str(db.address(f"G{i}")),
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
                "key": str(db.address(f"I{i}")),
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
    print(
        "Xin lưu ý rằng Olympia chỉ cho phép có 3 câu hỏi phụ (xem https://duong-len-dinh-olympia.fandom.com/vi/wiki/Lu%E1%BA%ADt_ch%C6%A1i#24,_25), nhưng Olympus hỗ trợ đến 6. owl sẽ chỉ nhập 3 câu hỏi đầu tiên."
    )
    for i in range(53, 56):
        output.append(
            {
                "prompt": db.address(f"B{i}"),
                "key": str(db.address(f"C{i}")),
                "score": 10,
                "time": 15,
                "media": None,
                "choices": [],
                "scoreFalse": 0,
                "explaination": "",
            }
        )

    output[42]["media"] = {
        "mediaType": "image",
        "uri": "/tangtoc/q1.png",
    }
    output[43]["media"] = {
        "mediaType": "image",
        "uri": "/tangtoc/q2.png",
    }
    output[44]["media"] = {
        "mediaType": "image",
        "uri": "/tangtoc/q3.png",
    }
    output[45]["media"] = {
        "mediaType": "video",
        "uri": "/tangtoc/q4.mp4",
    }

    with open(
        os.path.join("assets", "question_official.json"), "w", encoding="utf8"
    ) as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    # Only outputs default config.
    print(
        "Xin lưu ý rằng, vì định dạng Olympus không có cài đặt tên người chơi, owl sẽ để tên của họ thành mặc dịnh (Player 1, v.v.) và mật khẩu là 1234."
    )
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(
            {
                "listenOn": {"host": "localhost", "port": 6942},
                "devServer": {
                    "host": "localhost",
                    "port": 6699,
                },
                "serveDir": "serve",
                "staticDir": "static",
                "checkRPCTypes": True,
                "debug": True,
                "tickSpeed": 10,
                "gameAssets": [
                    "/tangtoc/q1.png",
                    "/tangtoc/q2.png",
                    "/tangtoc/q3.png",
                    "/tangtoc/q4.mp4",
                ],
                "credentials": [
                    {
                        "fullName": "Player 1",
                        "username": "player1",
                        "accessKey": "1234",
                    },
                    {
                        "fullName": "Player 2",
                        "username": "player2",
                        "accessKey": "1234",
                    },
                    {
                        "fullName": "Player 3",
                        "username": "player3",
                        "accessKey": "1234",
                    },
                    {
                        "fullName": "Player 4",
                        "username": "player4",
                        "accessKey": "1234",
                    },
                ],
                "game": {
                    "vcnv": {
                        "keyLength": len(
                            str(db.address("E42")).upper().replace(" ", "")
                        ),
                        "qualityPercentage": 85,
                        "keyResolution": {
                            "width": 784,
                            "height": 666,
                        },
                    }
                },
            },
            f,
            ensure_ascii=False,
            indent=4,
        )
    print("Đã viết config.json")


if __name__ == "__main__":
    print("Đang nhập câu hỏi...")
    f = pylightxl.readxl("config.xlsx")
    db = f.ws(f.ws_names[0])
    if db.address("A1") == "ĐƯỜNG ĐUA XANH - CÀI ĐẶT CHƯƠNG TRÌNH":
        if db.address("O1") == "v0.2":
            print("Phát hiện config.xlsx là định dạng DDX, phiên bản 0.2")
            ddx_loaderv02(db)
        else:
            print("Phát hiện config.xlsx là định dạng DDX, phiên bản 0.1")
            ddx_loaderv01(db)
    elif db.address("A3") == "Tên trận/giải đấu (nhập vào ô bên phải) [BẮT BUỘC]":
        print("Phát hiện config.xlsx là định dạng Olympus.")
        olympus_loader(db)
    else:
        print(
            "Định dạng tệp cài đặt không xác định. Chỉ hỗ trợ định dạng DDX và Olympus Online."
        )
        exit(0)
    print("Nhập câu hỏi hoàn thành.")

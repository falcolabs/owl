import json

with open("config.json", "r", encoding="utf8") as f:
    cfg = json.load(f)
    with open("frontend/.env", "w", encoding="utf8") as g:
        g.write(
            f'VITE_WSENDPOINT="{cfg["listenOn"]["host"]}:{cfg["listenOn"]["port"]}"'
        )
    print(
        f'export HOST={cfg["devServer"]["host"]};export PORT={cfg["devServer"]["port"]}'
    )

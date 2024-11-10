from PIL import Image
import math
import base64
from io import BytesIO
from config import config

BASE_IMG = Image.open("../assets/vcnv/key.png")
width, height = (
    config().game.vcnv.keyResolution.width,
    config().game.vcnv.keyResolution.height,
)
BASE_IMG = BASE_IMG.resize((width, height))

FRAG_1 = Image.open("../assets/vcnv/one.png")
FRAG_2 = Image.open("../assets/vcnv/two.png")
FRAG_3 = Image.open("../assets/vcnv/three.png")
FRAG_4 = Image.open("../assets/vcnv/four.png")
FRAG_M = Image.open("../assets/vcnv/center.png")


def get_imgdata(fragments: list[str]) -> str:
    out = BASE_IMG.copy()
    if "1" in fragments:
        out.paste(FRAG_1, (0, -1), FRAG_1)
    if "2" in fragments:
        out.paste(FRAG_2, (math.floor(width / 2), -1), FRAG_2)
    if "3" in fragments:
        out.paste(FRAG_3, (0, math.floor(height / 2)), FRAG_3)
    if "4" in fragments:
        out.paste(FRAG_4, (math.floor(width / 2), math.floor(height / 2)), FRAG_4)
    if "M" in fragments:
        out.paste(
            FRAG_M,
            (math.floor(width / 4), math.floor(height / 4)),
            FRAG_M,
        )
    buff = BytesIO()
    out = out.resize(
        (
            width // 2,
            height // 2,
        )
    )
    out.save(buff, "webp", quality=config().game.vcnv.qualityPercentage)
    return base64.b64encode(buff.getvalue()).decode("utf8")

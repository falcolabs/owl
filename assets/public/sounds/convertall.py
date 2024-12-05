import subprocess
import os
from pathlib import Path

if __name__ == "__main__":
    for i in os.listdir("unconverted"):
        print("Converting", i)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                os.path.join("unconverted", i),
                "-acodec",
                "libopus",
                "-f",
                "webm",
                Path(i).stem + ".webm",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
    print("Done!")

# the main server logic of owl, an engine for making gameshows.
# Copyright (C) 2024 Team Falco
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import engine
import logic.auth
import logic.khoidong
import logic.vcnv
import logic.tangtoc
import logic.vedich

import penguin
import config


def main():
    qbank = engine.QuestionBank()
    qbank.load("../assets/question_template.json")
    config.load("../config.json")
    penguin.set_error_hook()
    if config.config().debug:
        engine.set_log_level(engine.Level.DEBUG)

    show = penguin.Show(
        "Đáy xã hội 2",
        [
            engine.Part(logic.vedich.VeDich(), "vedich"),
            engine.Part(logic.tangtoc.TangToc(), "tangtoc"),
            engine.Part(logic.vcnv.VCNV(), "vcnv"),
            engine.Part(logic.khoidong.KhoiDong(), "khoidong"),
            engine.Part(logic.auth.Auth(), "auth"),
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

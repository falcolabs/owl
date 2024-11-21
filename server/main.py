# the main server logic of owl, an engine for making gameshows.
# Copyright (C) 2024 FalcoLabs
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

import engine
import penguin
import config


def main():
    qbank = engine.QuestionBank()
    qbank.load("../assets/question_test.json")
    config.load("../config.json")
    penguin.set_error_hook()
    if config.config().debug:
        engine.set_log_level(engine.Level.DEBUG)

    import logic.auth
    import logic.standby
    import logic.khoidong
    import logic.vcnv
    import logic.tangtoc
    import logic.vedich

    show = penguin.Show(
        "Đường đua xanh",
        [
            engine.Part(logic.auth.Auth(), "auth"),
            engine.Part(logic.standby.Standby(), "standby"),
            engine.Part(logic.khoidong.KhoiDong(), "khoidong"),
            engine.Part(logic.vcnv.VCNV(), "vcnv"),
            engine.Part(logic.tangtoc.TangToc(), "tangtoc"),
            engine.Part(logic.vedich.VeDich(), "vedich"),
        ],
        [engine.Player(c.username, c.fullName, 0) for c in config.config().credentials],
        config.config().tickSpeed,
        qbank,
    )

    show.start(
        config.config().listenOn,
        "dist",
        "static",
    )


if __name__ == "__main__":
    main()

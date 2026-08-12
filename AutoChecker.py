# This file is part of the daily-edited-checker distribution (https://github.com/miraclerin/daily-edited-checker).
# Copyright (c) 2026 miraclerin.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from time import sleep

from DailyModifiedChecker import DailyModifiedChecker


checker = DailyModifiedChecker()


while True:
    checker.run()
    sleep(checker.settings["process.update.time"])

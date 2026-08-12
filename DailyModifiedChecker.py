# This file is part of the daily-modified-checker distribution (https://github.com/miraclerin/daily-modified-checker).
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


import json
import os
from datetime import datetime


class DailyModifiedChecker():
    def __init__(self):
        self.load_settings("settings.json")

        self.settings: dict
        self.database: dict

    def run(self):
        self.load_database()

        to_check = self.get_paths_to_check()

        for i in to_check:
            self.write_date_in_database(i, self.get_file_date_when_modified(i))

        self.write_database()

    def load_settings(self, path):
        f = open(path, encoding="utf-8")
        self.settings = json.loads(f.read())
        f.close()

    def write_settings(self):
        f = open("settings.json", "w", encoding="utf-8")
        f.write(json.dumps(self.settings, indent=4, ensure_ascii=False))
        f.close()

    def load_database(self):
        f = open(self.settings["database.path"], encoding="utf-8")
        self.database = json.loads(f.read())
        f.close()

    def write_database(self):
        f = open(self.settings["database.path"], "w", encoding="utf-8")
        f.write(json.dumps(self.database, indent=4, ensure_ascii=False))
        f.close()

    def get_file_date_when_modified(self, file_path):
        f = datetime.fromtimestamp(os.path.getmtime(file_path))
        return (f.strftime("%Y"),
                f.strftime("%m"),
                f.strftime("%d"),
                f.strftime("%H:%M:%S"))

    def write_date_in_database(self, checked_file, date):
        # I think... it looks really bad
        if checked_file in self.database:
            if date[0] in self.database[checked_file]:
                if date[1] in self.database[checked_file][date[0]]:
                    if date[2] in self.database[checked_file][date[0]][date[1]]:
                        if self.settings["time.record"] and date[3] not in self.database[checked_file][date[0]][date[1]][date[2]]:
                            self.database[checked_file][date[0]][date[1]][date[2]].append(date[3])
                    else:
                        self.database[checked_file][date[0]][date[1]][date[2]] = [date[3]]
                else:
                    self.database[checked_file][date[0]][date[1]] = {date[2]: [date[3]]}
            else:
                self.database[checked_file][date[0]] = {date[1]: {date[2]: [date[3]]}}
        else:
            self.database[checked_file] = {date[0]: {date[1]: {date[2]: [date[3]]}}}

    def get_paths_to_check(self):
        f = open(self.settings["to_check.path"], encoding="utf-8")
        paths_to_check = f.read().split("\n")
        f.close()
        return paths_to_check


if __name__ == '__main__':
    main = DailyModifiedChecker()
    main.run()

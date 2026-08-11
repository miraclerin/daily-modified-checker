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

        f = open(self.settings["to_check.path"])
        to_check = f.read().split("\n")
        f.close()

        for i in to_check:
            self.write_date_in_database(i, self.get_file_date_when_modified(i))

        self.write_database()

    def load_settings(self, path):
        f = open(path)
        self.settings = json.loads(f.read())
        f.close()

    def write_settings(self):
        f = open("settings.json", "w")
        f.write(json.dumps(self.settings, indent=4))
        f.close()

    def load_database(self):
        f = open(self.settings["database.path"])
        self.database = json.loads(f.read())
        f.close()

    def write_database(self):
        f = open(self.settings["database.path"], "w")
        f.write(json.dumps(self.database, indent=4))
        f.close()

    def get_file_date_when_modified(self, file_path):
        return datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d")

    def write_date_in_database(self, checked_file, date):
        if checked_file in self.database:
            if date not in self.database[checked_file]:
                self.database[checked_file].append(date)
        else:
            self.database[checked_file] = [date]


if __name__ == '__main__':
    main = DailyModifiedChecker()
    main.run()

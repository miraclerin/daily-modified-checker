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


from datetime import datetime
from time import time
from colorama import Fore, Style, just_fix_windows_console
from json import JSONDecodeError, loads, dumps
from sys import platform

from DailyModifiedChecker import DailyModifiedChecker


class Visualizer():
    def __init__(self):
        self.today = datetime.today().strftime("%Y-%m-%d")
        self.day_of_week = int(datetime.today().strftime("%w"))
        self.week = int(datetime.today().strftime("%W"))
        self.year = int(datetime.today().strftime("%Y"))

        self.locale_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        self.locale_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        self.locale_errors = {"file.read": "Some file cannot be read.", "file.found": "Some file cannot be found.",
                              "to_check.incorrect": "to_check.txt is empty or incorrectly written. Refer to INSTRUCTION.txt to fix it.",
                              "year.range": "An year must be in range 1000...9998.", "year.notint": "Don't seem to be an year.{"}

        self.locale_other = {"prompt": "Type the year for which you want to view statistics: ",
                             "modified": "Modified", "modified.today": "Modified today"}

        self.checker: DailyModifiedChecker

    def run(self):
        self.checker = DailyModifiedChecker()
        
        self.load_locale()

        to_check = self.checker.get_paths_to_check()

        if to_check[0] == "":
            print(f"\n{Fore.YELLOW}[WARNING] {self.locale_errors["to_check.incorrect"]}{Style.RESET_ALL}\n")

        self.checker.run()

        print("\n")
        for file_path in to_check:
            print(f"\n{file_path}:\n")
            self.print_graph(self.year, self.get_graph(file_path, self.year))
            print()

        while True:
            try:
                the_year = int(input(self.locale_other["prompt"]))

                if the_year < 1000 or the_year >= 9999:
                    print(f"\n{Fore.RED}[ERROR] {self.locale_errors["year.range"]}{Style.RESET_ALL}\n")
                    continue

                print("\n")

                for file_path in to_check:
                    print(f"\n{file_path}:\n")
                    self.print_graph(the_year, self.get_graph(file_path, the_year))
                    print()

            except ValueError:
                print(f"\n{Fore.RED}[ERROR] {self.locale_errors["year.notint"]}{Style.RESET_ALL}\n")

    def get_graph(self, file_path, year):
        self.checker.load_database()
        data = self.checker.database[file_path]

        week = 1

        is_graph_done = False
        graph = []

        while not is_graph_done:
            for day in range(1, 8):
                try:
                    date = datetime.fromisocalendar(year, week, day).strftime("%Y-%m-%d")
                except ValueError:
                    if week == 54:
                            is_graph_done = True
                            break
                    elif datetime.fromisocalendar(year, week - 1, 7).strftime("%d") != 31:
                        date = datetime.fromisocalendar(year + 1, 1, day).strftime("%Y-%m-%d")
                    else:
                        is_graph_done = True
                        break
                if day == 1:
                    graph.append([])

                if str(year) != date[:date.find("-")]:
                    graph[week - 1].append("   ")
                elif date in data:
                    graph[week - 1].append("[#]")
                else:
                    graph[week - 1].append("[ ]")

            week += 1

        graph = [[j[i] for j in graph] for i in range(7)]

        return graph

    def print_graph(self, year, graph):
        if graph[self.day_of_week - 1][self.week] == "[#]":
            graph[self.day_of_week - 1][self.week] = f"[{Fore.YELLOW}#{Style.RESET_ALL}]"

        graph = [[(f"[{Fore.GREEN}#{Style.RESET_ALL}]" if j == "[#]" else j) for j in i] for i in graph]

        week = 0
        week_month_dict = {1: f"{self.locale_months[0]} 1 "}
        while True:
            week += 1
            try:
                date = datetime.fromisocalendar(year, week, 1).strftime("%m-%d")
            except ValueError:
                break
            month = int(date[:date.find("-")])
            day = int(date[date.find("-") + 1:])
            if day in range(8) and month > 1:
                week_month_dict[week] = f"{self.locale_months[month - 1]} {day} "

        week_month_str = ""
        week_counter = 1
        while week_counter < 54:
            if week_counter in week_month_dict:
                week_month_str += week_month_dict[week_counter]
                week_counter += 2
            week_month_str += " " * 3
            week_counter += 1

        print(f"\t\t{week_month_str}")
        print("\t\t" + "".join(graph[0]))
        print(f"\t{self.locale_days[1]}\t" + "".join(graph[1]))
        print("\t\t" + "".join(graph[2]))
        print(f"\t{self.locale_days[3]}\t" + "".join(graph[3]))
        print("\t\t" + "".join(graph[4]))
        print(f"\t{self.locale_days[5]}\t" + "".join(graph[5]))
        print("\t\t" + "".join(graph[6]))
        print()
        print(f"\t\t\t{Fore.GREEN}{self.locale_other["modified"]}\t\t{Fore.YELLOW}{self.locale_other["modified.today"]}{Style.RESET_ALL}")

    def load_locale(self):
        try:
            f = open(self.checker.settings["locale_path"], encoding="utf-8")
            to_load = loads(f.read())

            self.locale_months = to_load["months"]
            self.locale_days = to_load["days"]
            self.locale_errors = to_load["errors"]
            self.locale_other = to_load["other"]

            f.close()

        except FileNotFoundError:
            f = open(self.checker.settings["locale_path"], "w")
            to_write = {"months": self.locale_months, "days": self.locale_days, "errors": self.locale_errors, "other": self.locale_other}
            f.write(dumps(to_write, indent=4))

        except KeyError:
            self.checker.settings["locale_path"] = "visualizer_locale_en_US.json"
            self.checker.write_settings()
            self.load_locale()


if __name__ == '__main__':
    if platform == "win32":
        just_fix_windows_console()

    print("Daily Modified Checker Visualizer  Copyright (C) 2026  miraclerin")
    try:
        visualizer = Visualizer()
        visualizer.run()
    except JSONDecodeError:
        print(f"\n{Fore.RED}[ERROR] {visualizer.locale_errors["file.read"]}{Style.RESET_ALL}\n")
        input()
    except FileNotFoundError:
        print(f"\n{Fore.RED}[ERROR] {visualizer.locale_errors["file.found"]}{Style.RESET_ALL}\n")
        input()

# Daily Modified Checker
A simple application that automatically records file dates modified in a database and displays them beautifully.

In other words, the program monitors for the file changes every 10 minutes, and if changes are detected, it marks the day of the change in the database.

## Contribution
The application was created primarily for myself, and uploaded to GitHub for easy distribution to my friends. But feel free to suggest improvements and fork the repository.

## How to use
See [INSTRUCTION.txt](https://github.com/miraclerin/daily-modified-checker/blob/main/INSTRUCTION.txt) (или [ИНСТРУКЦИЯ.txt](https://github.com/miraclerin/daily-modified-checker/blob/main/%D0%98%D0%9D%D0%A1%D0%A2%D0%A0%D0%A3%D0%9A%D0%A6%D0%98%D0%AF.txt)).

## Configuration
The `settings.json` file allow you to change paths to `database.json`, to `to_check.txt` and change the AutoChecker process update time.

The `to_check.txt` must contain the paths to the files which date modified you want to record in a database.

## License
Distributed under the GNU GPL-3.0. See [LICENSE](https://github.com/miraclerin/daily-modified-checker/blob/main/LICENSE) for more information.

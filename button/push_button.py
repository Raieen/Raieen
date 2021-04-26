#!/usr/bin/python

"""Update the score of the GitHub user and regenerate the README file
to be committed as a GitHub Action.

Run this script with the GitHub user name that pressed the button,
excluding the '@' character.

Ex: ./push_button.py Raieen
"""
import sys
import time
import os
import shutil

# Replaced in README.md with actual content
TEMPLATE_RECENT="$TEMPLATE_RECENT"
TEMPLATE_LEADERBOARD="$TEMPLATE_LEADERBOARD"

# Files
LOG_FILE="log.txt"
LAST_PRESSED_FILE="last_pressed.txt"
SCORE_FILE="score.txt"
TEMPLATE_FILE="TEMPLATE.md"
README_FILE="../README.md"

# Bound constants in hours
# Red is implicitly anything strictly greater than ORANGE_UPPER
# Green is implicitly anything strictly lower than YELLOW_LOWER
ORANGE_UPPER = 99
ORANGE_LOWER = 50

YELLOW_UPPER = 49
YELLOW_LOWER = 30

def replace_in_file(file_name, find, replace):
    """
    Replace 'find' with 'replace' in the given file_name.
    """
    with open(file_name, encoding="utf8") as open_file:
        result=open_file.read().replace(find, replace)
        open_file.close()

    with open(file_name, "w", encoding="utf8") as open_file:
        open_file.write(result)
        open_file.close()


def get_display_name(username, score):
    """
    Return a string formatted as 'emoji (score) username'.

    The emoji depends on the score.
    """
    emoji = "error"
    if score > ORANGE_UPPER:
        emoji = "\U0001F7E5" # Red Square
    elif ORANGE_LOWER <= score <= ORANGE_UPPER:
        emoji = "\U0001F7E7" # Orange Square
    elif YELLOW_LOWER <= score <= YELLOW_UPPER:
        emoji = "\U0001F7E8" # Yellow Square
    else:
        emoji="\U0001F7E9" # Green Square
    return '{emoji} ({score}) {username}'.format(emoji=emoji, score=score, username=username)


def get_score(current_seconds, last_seconds):
    """
    Return the score computed as
    score = int ((current_seconds - last_seconds) / 60 / 60 * 1.5)
    """
    return int((current_seconds - last_seconds) // 60 // 60 * 1.5)


def append_log_last_pressed(username, score, timestamp):
    """
    Append the button press to the log file and update the
    last pressed file.
    """
    with open(LOG_FILE, "a") as log_file:
        log_file.write(username + "," + str(score) + "," + str(timestamp) + "\n")
        log_file.close()

    with open(LAST_PRESSED_FILE, "w") as last_pressed:
        last_pressed.write(str(timestamp))
        last_pressed.close()



def increment_score(username, score):
    """
    Add score to the user's score in the score file.
    """
    with open(SCORE_FILE, "r+") as score_file:
        replace_line = ""
        for line in score_file:
            if line.startswith(username):
                replace_line = line
                break

        if replace_line:
            old_score = int(replace_line.split(",")[1])
            new_line = "{},{}\n".format(username, str(score + old_score))
            replace_in_file(SCORE_FILE, replace_line, new_line)
        else:
            score_file.write("{},{}\n".format(username, str(score)))

        score_file.close()


def generate_recent():
    """
    Generate a user displayed string of the 5 most recent
    entries in the log file.
    """
    recent_lines = os.popen("tac {} | head -n 5".format(LOG_FILE)).read().split("\n")[:-1]
    recent_result = ""
    for recent_entry in recent_lines:
        entry_split = recent_entry.split(",")
        recent_result += get_display_name(entry_split[0], int(entry_split[1])) + ", "

    recent_result = recent_result[:-2]
    return recent_result

def generate_leaderboard():
    """
    Generate a user displayed string of the highest scoring 5
    entries in the score file.
    """
    leaderboard_lines = os.popen("sort -t , -k2 {} -g -r | head -n 5".format(SCORE_FILE))\
        .read().split("\n")[:-1]
    leaderboard_result = ""

    for leaderboard_entry in leaderboard_lines:
        entry_split = leaderboard_entry.split(",")
        leaderboard_result += "1. {}\n"\
            .format(get_display_name(entry_split[0], int(entry_split[1])))
    return leaderboard_result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing GitHub Username")
        sys.exit(1)

    gh_username = "@" + sys.argv[1]
    current_time = int(time.time())
    last_pressed_time = current_time

    if os.path.exists(LAST_PRESSED_FILE):
        with open(LAST_PRESSED_FILE) as last_file:
            last_pressed_time = int(last_file.readline())

    current_score = get_score(current_time, last_pressed_time)

    # Bookkeeping
    append_log_last_pressed(gh_username, current_score, current_time)
    increment_score(gh_username, current_score)

    # Generate README
    RECENT_STR = generate_recent()
    LEADERBOARD_STR = generate_leaderboard()

    shutil.copyfile(TEMPLATE_FILE, README_FILE)
    replace_in_file(README_FILE, TEMPLATE_RECENT, RECENT_STR)
    replace_in_file(README_FILE, TEMPLATE_LEADERBOARD, LEADERBOARD_STR)

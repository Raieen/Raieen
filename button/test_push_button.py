import unittest
import os
import push_button


class TestPushButton(unittest.TestCase):

    def test_replace_in_file_present(self):
        with open("test_replace_in_file.txt", "w+") as write_file:
            write_file.write("Hello World")
            write_file.flush()
            push_button.replace_in_file("test_replace_in_file.txt", "Hello", "Hi")

        with open("test_replace_in_file.txt", "r") as read_file:
            self.assertEqual(read_file.readlines(), ["Hi World"])
        os.remove("test_replace_in_file.txt")

    def test_replace_in_file_absent(self):
        with open("test_replace_in_file.txt", "w+") as write_file:
            write_file.write("Hello World")
            write_file.flush()
            push_button.replace_in_file("test_replace_in_file.txt", "123", "Hi")

        with open("test_replace_in_file.txt", "r") as read_file:
            self.assertEqual(read_file.readlines(), ["Hello World"])
        os.remove("test_replace_in_file.txt")

    def test_get_display_name(self):
        self.assertEqual(push_button.get_display_name("username", 1), "\U0001F7E9 (1) username")

    def test_get_score_zero(self):
        self.assertEqual(push_button.get_score(60, 0), 0)

    def test_get_score_one(self):
        self.assertEqual(push_button.get_score(7200, 0), 3)

    def test_append_log_last_pressed(self):
        push_button.LOG_FILE = "test_log.txt"
        push_button.LAST_PRESSED_FILE = "test_last.txt"
        push_button.append_log_last_pressed("username", 0, 1)

        with open(push_button.LOG_FILE, "r") as log_file:
            self.assertEqual(log_file.readlines(), ["username,0,1\n"])
        with open(push_button.LAST_PRESSED_FILE, "r") as last_file:
            self.assertEqual(last_file.readlines(), ["1"])

        os.remove(push_button.LOG_FILE)
        os.remove(push_button.LAST_PRESSED_FILE)

    def test_increment_score_new(self):
        push_button.SCORE_FILE = "test_score.txt"
        with open(push_button.SCORE_FILE, "w+") as write_file:
            write_file.write("")
            write_file.flush()
        push_button.increment_score("username", 1)

        with open(push_button.SCORE_FILE, "r") as score_file:
            self.assertEqual(score_file.readlines(), ["username,1\n"])

        os.remove(push_button.SCORE_FILE)

    def test_increment_score_existing(self):
        push_button.SCORE_FILE = "test_score.txt"
        with open(push_button.SCORE_FILE, "w+") as write_file:
            write_file.write("username,1")
            write_file.flush()
        push_button.increment_score("username", 1)

        with open(push_button.SCORE_FILE, "r") as score_file:
            self.assertEqual(score_file.readlines(), ["username,2\n"])

        os.remove(push_button.SCORE_FILE)

    def test_generate_recent(self):
        push_button.LOG_FILE = "test_log.txt"
        with open(push_button.LOG_FILE, "w+") as write_file:
            write_file.write("user1,0,1\n")
            write_file.flush()
        self.assertEqual(push_button.generate_recent(), "\U0001F7E9 (0) user1")
        os.remove(push_button.LOG_FILE)

    def test_generate_recent_many(self):
        push_button.LOG_FILE = "test_log.txt"
        with open(push_button.LOG_FILE, "w+") as write_file:
            write_file.write("user6,0,1\nuser5,0,1\nuser4,0,1\nuser3,0,1\nuser2,0,1\nuser1,0,1\n")
            write_file.flush()
        self.assertEqual(push_button.generate_recent(), "\U0001F7E9 (0) user1, \U0001F7E9 (0) user2, \U0001F7E9 (0) user3, \U0001F7E9 (0) user4, \U0001F7E9 (0) user5")
        os.remove(push_button.LOG_FILE)

    def test_generate_leaderboard(self):
        push_button.SCORE_FILE = "test_score.txt"
        with open(push_button.SCORE_FILE, "w+") as write_file:
            write_file.write("user1,0\n")
            write_file.flush()
        self.assertEqual(push_button.generate_leaderboard(), "1. \U0001F7E9 (0) user1\n")
        os.remove(push_button.SCORE_FILE)

    def test_generate_leaderboard_many(self):
        push_button.SCORE_FILE = "test_score.txt"
        with open(push_button.SCORE_FILE, "w+") as write_file:
            write_file.write("user1,1\nuser2,2\nuser3,3\nuser4,4\nuser5,5\nuser6,6\n")
            write_file.flush()
        self.assertEqual(push_button.generate_leaderboard(), "1. \U0001F7E9 (6) user6\n1. \U0001F7E9 (5) user5\n1. \U0001F7E9 (4) user4\n1. \U0001F7E9 (3) user3\n1. \U0001F7E9 (2) user2\n")
        os.remove(push_button.SCORE_FILE)

if __name__ == '__main__':
    unittest.main()

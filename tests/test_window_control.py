
import unittest
from unittest.mock import patch

from agent.jarvis import Jarvis
from tools.system import close_window


def make_window(hwnd, title, pid=1000, process="notepad.exe"):
    return {
        "hwnd": hwnd,
        "title": title,
        "pid": pid,
        "process": process,
    }


class CloseWindowTests(unittest.TestCase):

    @patch("tools.system._get_open_windows", return_value=[])
    def test_window_not_found(self, mock_windows):
        result = close_window("Missing Window")

        self.assertEqual(
            result,
            "No open window matched 'Missing Window'.",
        )

    @patch("tools.system._get_open_windows", return_value=[])
    def test_empty_title(self, mock_windows):
        result = close_window("   ")

        self.assertEqual(result, "Please provide a window title.")

    @patch("tools.system._get_open_windows")
    def test_multiple_matching_windows_are_not_closed(self, mock_windows):
        mock_windows.return_value = [
            make_window(101, "Report - Notepad", 1001),
            make_window(102, "Report - Notepad", 1002),
        ]

        result = close_window("Report - Notepad")

        self.assertIn("Multiple windows matched", result)
        self.assertIn("PID: 1001", result)
        self.assertIn("PID: 1002", result)

    @patch("tools.system.ctypes.windll.user32.PostMessageW", return_value=1)
    @patch("tools.system._get_open_windows")
    def test_exact_match_sends_close_request(
        self, mock_windows, mock_post_message
    ):
        mock_windows.return_value = [
            make_window(101, "Untitled - Notepad", 1001),
            make_window(102, "Calculator", 1002, "Calculator.exe"),
        ]

        result = close_window("Untitled - Notepad")

        self.assertIn("Close request sent", result)
        self.assertIn("Untitled - Notepad", result)
        mock_post_message.assert_called_once()

    @patch("tools.system.ctypes.windll.user32.PostMessageW", return_value=0)
    @patch("tools.system._get_open_windows")
    def test_failed_close_request_is_reported(
        self, mock_windows, mock_post_message
    ):
        mock_windows.return_value = [
            make_window(101, "Untitled - Notepad", 1001),
        ]

        result = close_window("Untitled - Notepad")

        self.assertIn("Windows could not send a close request", result)

    @patch("tools.system.ctypes.windll.user32.PostMessageW", return_value=1)
    @patch("tools.system._get_open_windows")
    def test_exact_match_is_preferred_over_partial_matches(
        self, mock_windows, mock_post_message
    ):
        mock_windows.return_value = [
            make_window(101, "Notepad", 1001),
            make_window(102, "Untitled - Notepad", 1002),
        ]

        result = close_window("Notepad")

        self.assertIn("Close request sent to 'Notepad'", result)
        mock_post_message.assert_called_once()


class WindowCommandRoutingTests(unittest.TestCase):

    def setUp(self):
        self.jarvis = Jarvis()

    def test_window_list_phrases(self):
        for command in (
            "open windows",
            "show windows",
            "list open windows",
        ):
            with self.subTest(command=command):
                result = self.jarvis.detect_simple_tool(command)

                self.assertEqual(
                    result,
                    {
                        "tool": "list_open_windows",
                        "arguments": {},
                    },
                )

    def test_close_window_phrase(self):
        result = self.jarvis.detect_simple_tool(
            "close window titled Untitled - Notepad"
        )

        self.assertEqual(
            result,
            {
                "tool": "close_window",
                "arguments": {"title": "untitled - notepad"},
            },
        )


if __name__ == "__main__":
    unittest.main()
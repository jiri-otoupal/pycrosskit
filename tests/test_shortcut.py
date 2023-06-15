import os
import unittest

from pycrosskit.shortcuts import Shortcut


class Test_Shortcuts(unittest.TestCase):
    def test_exec_args_splitting(self):
        """Tests to make sure the target file
        and arguments are split correctly"""

        sh = Shortcut(
            "SplitTest",
            "\"file name with spaces.py\" --and --args 'with options.txt'",
            desktop=True,
        )
        self.assertEqual("file name with spaces.py", sh.exec_path)
        self.assertEqual("--and --args 'with options.txt'", sh.arguments)

        Shortcut.delete("SplitTest", desktop=True)

    def test_create_desktop(self):
        """Test Creation of shortcut with only desktop option"""

        sh = Shortcut("Test", "__init__.py", desktop=True)
        self.assertEqual(True, os.path.exists(sh.desktop_path))

    def test_delete_desktop(self):
        """Test Deletion of shortcut with only desktop option"""

        desktop, _ = Shortcut.delete("Test", desktop=True)
        self.assertEqual(True, not os.path.exists(desktop))

    def test_create_startmenu(self):
        """Test Creation of shortcut with only startmenu option"""

        sh = Shortcut("Test", "__init__.py", start_menu=True)
        self.assertEqual(True, os.path.exists(sh.startmenu_path))

    def test_delete_startmenu(self):
        """Test Deletion of shortcut with only startmenu option"""

        _, startmenu = Shortcut.delete("Test", start_menu=True)
        self.assertEqual(True, not os.path.exists(startmenu))

    def test_create_both(self):
        """Test Creation of shortcut with both options"""

        sh = Shortcut("Test", "__init__.py", desktop=True, start_menu=True)
        self.assertEqual(True, os.path.exists(sh.desktop_path))
        self.assertEqual(True, os.path.exists(sh.startmenu_path))

    def test_delete_both(self):
        """Test Deletion of shortcut with both options"""

        desktop, start_menu = Shortcut.delete("Test", desktop=True, start_menu=True)
        self.assertEqual(True, not os.path.exists(desktop))
        self.assertEqual(True, not os.path.exists(start_menu))


if __name__ == "__main__":
    unittest.main()

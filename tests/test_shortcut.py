import os
import unittest

from pycrosskit.shortcuts import Shortcut


class Test_Shortcuts(unittest.TestCase):
    def test_exec_args_splitting(self):
        sh = Shortcut(
            "SplitTest",
            "file name with spaces.py --and --args 'with options.txt'",
            desktop=True,
        )
        self.assertEqual("file name with spaces.py", sh.exec_path)
        self.assertEqual("--and --args 'with options.txt'", sh.arguments)

        desktop, _ = Shortcut.delete("SplitTest", desktop=True)

    def test_create_desktop(self):
        sh = Shortcut("Test", "__init__.py", desktop=True)
        self.assertEqual(True, os.path.exists(sh.desktop_path))

    def test_delete_desktop(self):
        desktop, _ = Shortcut.delete("Test", desktop=True)
        self.assertEqual(True, not os.path.exists(desktop))

    def test_create_startmenu(self):
        sh = Shortcut("Test", "__init__.py", start_menu=True)
        self.assertEqual(True, os.path.exists(sh.startmenu_path))

    def test_delete_startmenu(self):
        _, startmenu = Shortcut.delete("Test", start_menu=True)
        self.assertEqual(True, not os.path.exists(startmenu))

    def test_create_both(self):
        sh = Shortcut("Test", "__init__.py", desktop=True, start_menu=True)
        self.assertEqual(True, os.path.exists(sh.desktop_path))
        self.assertEqual(True, os.path.exists(sh.startmenu_path))

    def test_delete_both(self):
        desktop, start_menu = Shortcut.delete("Test", desktop=True, start_menu=True)
        self.assertEqual(True, not os.path.exists(desktop))
        self.assertEqual(True, not os.path.exists(start_menu))


if __name__ == "__main__":
    unittest.main()

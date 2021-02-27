import os
import unittest

from pycrosskit.shortcuts import Shortcut


class Test_Win_Shortcut(unittest.TestCase):

    def test_create_desktop(self):
        try:
            sh = Shortcut("Test", "__init__.py", desktop=True)
            self.assertEqual(True, os.path.exists(sh.desktop_path))
        except:
            self.assertEqual(True, False)

    def test_delete_desktop(self):
        try:
            desktop, startmenu = Shortcut.delete("Test", desktop=True)
            self.assertEqual(True, not os.path.exists(desktop))
        except:
            self.assertEqual(True, False)

    def test_create_startmenu(self):
        try:
            sh = Shortcut("Test", "__init__.py", start_menu=True)
            self.assertEqual(True, os.path.exists(sh.startmenu_path))
        except:
            self.assertEqual(True, False)

    def test_delete_startmenu(self):
        try:
            desktop, startmenu = Shortcut.delete("Test", start_menu=True)
            self.assertEqual(True, not os.path.exists(startmenu))
        except:
            self.assertEqual(True, False)

    def test_create_both(self):
        try:
            sh = Shortcut("Test", "__init__.py", desktop=True, start_menu=True)
            self.assertEqual(True, os.path.exists(sh.desktop_path))
            self.assertEqual(True, os.path.exists(sh.startmenu_path))
        except:
            self.assertEqual(True, False)

    def test_delete_both(self):
        try:
            desktop, startmenu = Shortcut.delete("Test", desktop=True, start_menu=True)
            self.assertEqual(True, not os.path.exists(desktop))
            self.assertEqual(True, not os.path.exists(startmenu))
        except:
            self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()

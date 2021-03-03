import unittest

from pycrosskit.envariables import SysEnv
from pycrosskit.shortcuts import Shortcut


class TestEnvVars(unittest.TestCase):

    def test_set_var(self):
        try:
            SysEnv.set_var("test", "test")
        except:
            self.fail("")

    def test_get_var(self):
        self.assertEqual(SysEnv.get_var("test"), "test")

    def test_get_rm_var(self):
        self.assertEqual(SysEnv.get_var("test", delete=True), "test")
        try:
            SysEnv.get_var("test")
            self.fail()
        except FileNotFoundError:
            pass

    def test_get_var_sub_key(self):
        if Shortcut.get_platform() == "win":
            SysEnv.set_var("test", "test", subkey="test")
            self.assertEqual(SysEnv.get_var("test", sub_key="test"), "test")


if __name__ == '__main__':
    unittest.main()

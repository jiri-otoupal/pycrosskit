import os
import unittest

from pycrosskit.envariables import SysEnv


class TestEnvVars(unittest.TestCase):
    def test_set_var(self):
        try:
            SysEnv().set("test", "test")
        except:
            self.fail("")

    def test_get_var(self):
        SysEnv().set("test", "test")
        self.assertEqual(SysEnv().get("test"), "test")

    def test_get_rm_var(self):
        SysEnv().set("test", "test")
        with open("~/.bashrc", "r") as f:
            lines = f.read(9999999)
            self.assertTrue("export test=" in lines)
        self.assertEqual(SysEnv().get("test"), "test")
        SysEnv().unset("test")

        with open("~/.bashrc", "r") as f:
            lines = f.read(9999999)
            self.assertFalse("export test=" in lines)

        try:
            SysEnv().get("test")
            self.fail()
        except Exception:
            pass


if __name__ == "__main__":
    if os.name != "nt":
        unittest.main()

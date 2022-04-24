import os
import unittest

from pycrosskit.env_platforms.var_exceptions import VarNotFound
from pycrosskit.envariables import SysEnv


class WindowsVarsTest(unittest.TestCase):
    def test_set_var(self):
        try:
            SysEnv().set("test", "test", registry=False)
        except:
            self.fail("")

    def test_get_var(self):
        SysEnv().set("test", "test")
        self.assertEqual(SysEnv().get("test", registry=False), "test")

    def test_get_var_default(self):
        SysEnv().unset("test", registry=True, silent=True)
        var = SysEnv().get("test", None, registry=True)
        self.assertEqual(var, None)

    def test_get_var_remove(self):
        SysEnv().set("test", "test", registry=False)
        value = SysEnv().get("test", registry=False)
        self.assertTrue(value, "test")
        with self.assertRaises(VarNotFound):
            SysEnv().unset("test")

    def test_get_var_remove_fail(self):
        SysEnv().unset("test", registry=False, silent=True)
        with self.assertRaises(VarNotFound):
            SysEnv().unset("test", registry=False)


if __name__ == '__main__':
    if os.name == "nt":
        unittest.main()

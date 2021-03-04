import unittest

from pycrosskit.envariables import SysEnv


class TestEnvVars(unittest.TestCase):

    def test_set_var(self):
        try:
            SysEnv.set_var("test", "test")
        except:
            self.fail("")

    def test_get_var(self):
        SysEnv.set_var("test", "test")
        self.assertEqual(SysEnv.get_var("test"), "test")

    def test_get_rm_var(self):
        SysEnv.set_var("test", "test")
        self.assertEqual(SysEnv.get_var("test", delete=True), "test")
        try:
            SysEnv.get_var("test")
            self.fail()
        except Exception:
            pass


if __name__ == '__main__':
    unittest.main()

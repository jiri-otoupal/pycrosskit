import unittest

from pycrosskit.envariables import SysEnv


class WindowsVarsTest(unittest.TestCase):
    def test_set_var(self):
        try:
            SysEnv.set_var("test", "test", registry=False)
        except:
            self.fail("")

    def test_get_var(self):
        SysEnv.set_var("test", "test")
        self.assertEqual(SysEnv.get_var("test", registry=False), "test")


if __name__ == '__main__':
    unittest.main()

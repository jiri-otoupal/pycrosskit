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

    def test_get_var_remove(self):
        SysEnv.set_var("test", "test", registry=False)
        self.assertTrue(SysEnv.get_var("test", registry=False, delete=True), "test")

    def test_get_var_remove_fail(self):
        SysEnv.set_var("test", "test", registry=True)
        with self.assertRaises(FileNotFoundError):
            SysEnv.get_var("test", registry=False, delete=True)


if __name__ == '__main__':
    unittest.main()

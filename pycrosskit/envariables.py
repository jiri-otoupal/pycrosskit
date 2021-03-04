import os
import subprocess

from pycrosskit.shortcuts import Shortcut


class SysEnv:
    default_reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    @staticmethod
    def get_var(name, reg_path=default_reg_path, delete=False):
        """
        Get Environment Variable
        :param name: Variable Name
        :param reg_path: Register path for windows
        :param delete: Delete after read
        :return: Value from variable
        :rtype: str
        """
        if Shortcut.get_platform() == "win":
            import winreg
            root = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            policy_key = winreg.OpenKeyEx(root, reg_path)
            value = winreg.QueryValue(policy_key, name)
            if delete:
                winreg.DeleteKey(policy_key, name)
            root.Close()
            return value
        else:
            value = subprocess.check_output(["echo", "$" + name])[1:-1].decode("utf-8")
            if delete:
                os.system("unset " + name)
            return value

    @staticmethod
    def set_var(name, value, subkey="", reg_path=default_reg_path):
        """
        Set Environment Variable
        :param name: Variable Name
        :param value: Variable Value
        :param subkey: Sub-Key under key ( like file in folder )
        :param reg_path: Register path for windows
        """
        if Shortcut.get_platform() == "win":
            import winreg
            root = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKeyEx(root, reg_path, winreg.KEY_SET_VALUE)
            policy_key = winreg.CreateKey(key, name)
            winreg.SetValueEx(policy_key, subkey, 0, winreg.REG_SZ, value)
            root.Close()
        else:
            os.system("echo 'export " + name + "=" + value + "' >> ~/.bashrc ")

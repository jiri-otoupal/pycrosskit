import os
from winreg import ConnectRegistry, HKEY_CURRENT_USER, OpenKeyEx, CreateKey, REG_SZ, SetValueEx, KEY_SET_VALUE, \
    DeleteKey, QueryValueEx

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
            root = ConnectRegistry(None, HKEY_CURRENT_USER)
            policy_key = OpenKeyEx(root, reg_path)
            value, type_ = QueryValueEx(policy_key, name)
            if delete:
                DeleteKey(policy_key, name)
            root.Close()
            return value
        else:
            value = os.getenv(name)
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
            root = ConnectRegistry(None, HKEY_CURRENT_USER)
            key = OpenKeyEx(root, reg_path, KEY_SET_VALUE)
            policy_key = CreateKey(key, name)
            SetValueEx(policy_key, subkey, 0, REG_SZ, value)
            root.Close()
        else:
            os.system("echo 'export " + name + "=" + value + "' >> ~/.bashrc ")

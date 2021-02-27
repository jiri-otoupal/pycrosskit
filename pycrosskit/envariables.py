import os
from winreg import ConnectRegistry, HKEY_CURRENT_USER, OpenKeyEx, CreateKey, REG_SZ, SetValueEx, KEY_SET_VALUE, \
    DeleteKey, QueryValueEx


class SysEnv:
    default_reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    @staticmethod
    def get_var(key, reg_path=default_reg_path, delete=False):
        try:
            root = ConnectRegistry(None, HKEY_CURRENT_USER)
            policy_key = OpenKeyEx(root, reg_path)
            value, type_ = QueryValueEx(policy_key, key)
            if delete:
                DeleteKey(policy_key, key)
            root.Close()
            return value
        except OSError:
            value = os.getenv(key)
            if delete:
                os.system("unset " + key)
            return value

    @staticmethod
    def set_var(name, value, subkey="", reg_path=default_reg_path):
        try:
            root = ConnectRegistry(None, HKEY_CURRENT_USER)
            key = OpenKeyEx(root, reg_path, KEY_SET_VALUE)
            policy_key = CreateKey(key, name)
            SetValueEx(policy_key, subkey, 0, REG_SZ, value)
            root.Close()
        except OSError:
            os.system("echo 'export " + name + "=" + value + "' >> ~/.bashrc ")

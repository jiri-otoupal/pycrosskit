import os
import subprocess
import winreg
from typing import Any, Union

from pycrosskit.env_platforms.var_exceptions import VarNotFound


class WinVar:

    @classmethod
    def __get(cls, key: str, reg_path: str, registry: bool):
        if registry:
            policy_key = cls.__get_policy_key(reg_path)
            try:
                value = winreg.QueryValue(policy_key, str(key))
            except FileNotFoundError:
                raise VarNotFound("This Registry Path does not exists on this system",
                                  "Please check path in regedit.exe")
        else:
            value = str(subprocess.check_output("echo %" + key + "%", shell=True),
                        "utf-8") \
                .replace("\r\n", "").replace("%", "")
        return value

    @classmethod
    def __get_policy_key(cls, reg_path):
        root = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        policy_key = winreg.OpenKeyEx(root, reg_path)
        return policy_key

    @classmethod
    def __unset(cls, name: str, policy_key, registry: bool):
        if not registry:
            err = os.system("REG delete HKCU\Environment /F /V " + str(name))
            if err != 0:
                raise VarNotFound("Environment Variable not found")
        else:
            winreg.DeleteKey(policy_key, str(name))

    @classmethod
    def unset(cls, name,
              reg_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
              registry=True, silent=False):
        """
        Unsets variable from environment or registry
        :param name: Variable name
        :param reg_path: Register path for windows
        :param registry: Only for windows, if true variable is obtained from registry path
                        if false variable is obtained to environment variables
        :param silent: If unset should fail silently in case that variable does not exist
        """
        try:
            policy_key = cls.__get_policy_key(reg_path)
            cls.__unset(name, policy_key, registry)
        except FileNotFoundError as ex:
            if not silent:
                raise VarNotFound(str(ex))

    @classmethod
    def get(cls, key: str, default: Union[Any, VarNotFound] = VarNotFound,
            reg_path: str = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            registry: bool = True):
        """
        Get Environment Variable
        :param default: Value returned if not found
        ( raises VarNotFound exception if not set)
        :param key: Variable Name
        :param reg_path: Register path for windows
        :param registry: Only for windows, if true variable is obtained from registry path
                        if false variable is obtained to environment variables
        :return: Value from variable or None if failed
        :rtype: str or None
        """
        root = None

        try:
            value = cls.__get(key, reg_path, registry)
            if registry and root is not None:
                root.Close()
        except VarNotFound as ex:
            if default != VarNotFound:
                return default
            raise ex
        return value

    @classmethod
    def set(cls, key, value, subkey="",
            reg_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            registry=True, silent=False):
        """
        Set Environment Variable
        :param silent: If permission error should fail silently
        :param key: Variable Name
        :param value: Variable Value
        :param subkey: Sub-Key under key ( like file in folder )
        :param reg_path: Register path for windows
        :param registry: Only for windows, if true variable is set to registry path
                if false, variable is set to environment variables
        """
        if registry:
            import winreg
            root = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key_ex = winreg.OpenKeyEx(root, reg_path, winreg.KEY_SET_VALUE)
            try:
                policy_key = winreg.CreateKey(key_ex, key)
                winreg.SetValueEx(policy_key, subkey, 0, winreg.REG_SZ, value)
                root.Close()
            except PermissionError as ex:
                if not silent:
                    raise ex
        else:
            os.system("setx " + str(key) + " " + str(value))

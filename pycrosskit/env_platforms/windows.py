import logging
import os
import subprocess
import winreg
from typing import Any, Union

from pycrosskit.env_platforms.exceptions import VarNotFound


class WinVar:
    shell = "batch"
    logger: logging.Logger = None

    def __new__(cls, logger):
        cls.logger = logger
        return cls

    @classmethod
    def __get(cls, key: str, reg_path: str, registry: bool) -> str:
        if registry:
            policy_key, root = cls.__get_policy_key_readonly(reg_path)
            try:
                value = winreg.QueryValue(policy_key, str(key))
            except FileNotFoundError:
                raise VarNotFound(
                    "This Registry Path does not exists on this system",
                    "Please check path in regedit.exe",
                )
            finally:
                if root is not None:
                    root.Close()
        else:
            value = (
                str(subprocess.check_output("echo %" + key + "%", shell=True), "utf-8")
                .replace("\r\n", "")
                .replace("%", "")
            )

        return value

    @classmethod
    def __get_policy_key_readonly(
            cls, reg_path: str, reg_key=winreg.HKEY_CURRENT_USER
    ):
        root = winreg.ConnectRegistry(None, reg_key)
        policy_key = winreg.OpenKeyEx(root, reg_path)
        return policy_key, root

    @classmethod
    def __unset(cls, key: str, policy_key: winreg.HKEYType, registry: bool):
        if not registry:
            err = os.system(r"REG delete HKCU\Environment /F /V " + str(key))
            if err != 0:
                raise VarNotFound("Environment Variable not found")
        else:
            winreg.DeleteKey(policy_key, str(key))

    @classmethod
    def unset(
            cls,
            key,
            reg_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            registry=True,
            silent=False,
    ):
        """
        Unsets variable from environment or registry
        :param key: Variable name
        :param reg_path: Register path for windows
        :param registry: Only for windows, if true variable is obtained from registry path
                        if false variable is obtained to environment variables
        :param silent: If unset should fail silently in case that variable does not exist
        """
        try:
            cls.logger.debug(f"Unsetting system variable {key}")
            policy_key, _ = cls.__get_policy_key_readonly(reg_path)
            cls.__unset(key, policy_key, registry)
            cls.logger.debug(f"Finished Unsetting system variable {key}")
        except FileNotFoundError as ex:
            if not silent:
                cls.logger.debug(f"Unset of variable {key} failed")
                raise VarNotFound(str(ex))
            cls.logger.debug(f"Unset of variable {key} failed silently")

    @classmethod
    def get(
            cls,
            key: str,
            default: Union[Any, VarNotFound] = VarNotFound,
            reg_path: str = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            registry: bool = True,
    ) -> str:
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
        try:
            value = cls.__get(key, reg_path, registry)

            cls.logger.debug(f"Got variable {key} {value}")
        except VarNotFound as ex:
            if default != VarNotFound:
                cls.logger.debug(f"Returning default variable {key} not found or empty")
                return default
            cls.logger.debug(f"Variable {key} not found")
            raise ex
        return value

    @classmethod
    def set(
            cls,
            key,
            value,
            subkey="",
            reg_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            reg_key=winreg.HKEY_CURRENT_USER,
            registry=True,
            silent=False,
    ):
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
            root = winreg.ConnectRegistry(None, reg_key)
            key_ex = winreg.OpenKeyEx(root, reg_path, winreg.KEY_SET_VALUE)
            try:
                policy_key = winreg.CreateKey(key_ex, key)
                winreg.SetValueEx(policy_key, subkey, 0, winreg.REG_SZ, value)
                root.Close()
                cls.logger.debug(f"Set variable to registry {key} {value}")
            except PermissionError as ex:
                if not silent:
                    cls.logger.debug(f"Set variable to registry failed {key} {value}")
                    raise ex
                cls.logger.debug(
                    f"Set variable to registry failed silently " f"{key} {value}"
                )
        else:
            os.system("setx " + str(key) + " " + str(value))
            cls.logger.debug(f"Set variable {key} {value}")

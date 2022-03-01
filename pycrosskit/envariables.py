import os
import subprocess

from pycrosskit.shortcuts import Shortcut


class SysEnv:

    @staticmethod
    def get_var(name, reg_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", delete=False,
                registry=True):
        """
        Get Environment Variable
        :param name: Variable Name
        :param reg_path: Register path for windows
        :param delete: Delete after read
        :param registry: Only for windows, if true variable is obtained from registry path
                        if false variable is obtained to environment variables
        :return: Value from variable or None if failed
        :rtype: str or None
        """
        root = None
        policy_key = None
        if Shortcut.get_platform() == "win":
            import winreg
            if registry:
                root = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                policy_key = winreg.OpenKeyEx(root, reg_path)
                try:
                    value = winreg.QueryValue(policy_key, str(name))
                except FileNotFoundError:
                    print("This Registry Path does not exists on this system")
                    print("Please check path in regedit.exe")
                    return None
            else:
                value = str(subprocess.check_output("echo %" + name + "%", shell=True), "utf-8").replace("\r\n",
                                                                                                         "").replace(
                    "%", "")
            if delete:
                if not registry:
                    err = os.system("REG delete HKCU\Environment /F /V " + str(name))
                    if err != 0:
                        raise FileNotFoundError("Environment Variable not found")
                else:
                    winreg.DeleteKey(policy_key, str(name))
            if registry and root is not None:
                root.Close()
            return value
        else:
            value = subprocess.check_output(["echo", "$" + str(name)])[1:-1].decode("utf-8")
            if delete:
                os.system("unset " + str(name))
            return value

    @staticmethod
    def set_var(name, value, subkey="",
                reg_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                registry=True):
        """
        Set Environment Variable
        :param name: Variable Name
        :param value: Variable Value
        :param subkey: Sub-Key under key ( like file in folder )
        :param reg_path: Register path for windows
        :param registry: Only for windows, if true variable is set to registry path
                if false, variable is set to environment variables
        """
        if Shortcut.get_platform() == "win":
            if registry:
                import winreg
                root = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKeyEx(root, reg_path, winreg.KEY_SET_VALUE)
                try:
                    policy_key = winreg.CreateKey(key, name)
                    winreg.SetValueEx(policy_key, subkey, 0, winreg.REG_SZ, value)
                    root.Close()
                except PermissionError:
                    print("Python does not have permission to modify registry")
                    return
            else:
                os.system("setx " + str(name) + " " + str(value))
        else:
            os.system("echo 'export " + str(name) + "=" + str(value) + "' >> ~/.bashrc ")

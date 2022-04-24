import os
import subprocess

from pycrosskit.env_platforms.var_exceptions import VarNotFound


class LinVar:
    EXPORT_STRING: lambda key, value: f"export {key}=\"{value}\""

    @classmethod
    def fetch_bashrc_line(cls):
        """
        Generator that fetches bashrc lines one by one
        """
        with open("~/.bashrc", "r") as f:
            yield f.readline()

    @classmethod
    def unset(cls, key):
        """
        Unsets variable from environment
        :param key: Key of variable

        Can throw PermissionError if bashrc is not accessible
        """
        replacement_lines = []

        for line in cls.fetch_bashrc_line():

            # Way faster than regex
            # Do search without quotes

            if cls.EXPORT_STRING(key, "")[:-2] in line:
                continue

            replacement_lines.append(line)

        with open("~/.bashrc", "w") as f:
            f.writelines(replacement_lines)

    @classmethod
    def get(cls, key, default=VarNotFound):
        """
        Get Environment Variable
        :param key: Key of variable
        :param default: Returned if variable empty or undefined
        :return: 
        """
        value = subprocess.check_output([
            "/usr/bin/env",
            "bash",
            "-ic",
            f". ~/.bashrc && echo -n ${key}"
        ], stderr=subprocess.DEVNULL).decode("utf-8")
        if not value:
            if default == VarNotFound:
                raise VarNotFound("System Variable is empty or undefined")
            return default
        return value

    @classmethod
    def set(cls, key, value):
        """
        Set Environment Variable
        :param key: Key of variable
        :param value: Value to be set
        """
        os.system(f"echo '{cls.EXPORT_STRING(key, value)}' >> ~/.bashrc")

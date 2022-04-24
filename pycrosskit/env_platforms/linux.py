import logging
import os
import subprocess
from typing import Union, Any

from pycrosskit.env_platforms.exceptions import VarNotFound


class LinVar:
    logger = logging.getLogger("env_vars")
    EXPORT_STRING: lambda key, value: f"export {key}=\"{value}\""

    @classmethod
    def __fetch_bashrc_line(cls):
        """
        Generator that fetches bashrc lines one by one
        """
        with open("~/.bashrc", "r") as f:
            yield f.readline()

    @classmethod
    def unset(cls, key: str):
        """
        Unsets variable from environment
        :param key: Key of variable

        Can throw PermissionError if bashrc is not accessible
        """
        cls.logger.debug(f"Unsetting system variable {key}")

        replacement_lines = []

        for line in cls.__fetch_bashrc_line():

            # Way faster than regex
            # Do search without quotes

            if cls.EXPORT_STRING(key, "")[:-2] in line:
                continue

            replacement_lines.append(line)

        with open("~/.bashrc", "w") as f:
            f.writelines(replacement_lines)

        cls.logger.debug(f"Finished Unsetting system variable {key}")

    @classmethod
    def get(cls, key: str, default: Union[Any, VarNotFound] = VarNotFound):
        """
        Get Environment Variable
        :param key: Key of variable
        :param default: Returned if variable empty or undefined
        :return: 
        """
        value: str = subprocess.check_output(
            [
                "/usr/bin/env",
                "bash",
                "-ic",
                f". ~/.bashrc && echo -n ${key}"
            ], stderr=subprocess.DEVNULL).decode("utf-8")

        # Check for empty or unset variable
        if not value:

            if default == VarNotFound:
                cls.logger.debug(f"Variable {key} not found")
                raise VarNotFound("System Variable is empty or undefined")

            cls.logger.debug(f"Returning default variable {key} not found or empty")
            return default

        cls.logger.debug(f"Got variable {key} {value=}")
        return value

    @classmethod
    def set(cls, key: str, value: str):
        """
        Set Environment Variable
        :param key: Key of variable
        :param value: Value to be set
        """
        os.system(f"echo '{cls.EXPORT_STRING(key, value)}' >> ~/.bashrc")
        cls.logger.debug(f"Set variable {key} {value=}")

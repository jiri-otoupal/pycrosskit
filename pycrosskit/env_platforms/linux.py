import logging
import os
import subprocess
from typing import Union, Any, Tuple

from pycrosskit.env_platforms.exceptions import VarNotFound


class LinVar:
    shell = "bash"
    shell_file = "~/.bashrc"
    logger: logging.Logger = None

    EXPORT_STRING = lambda key, value: f'export {key}="{value}"'

    def __new__(cls, logger):
        cls.logger = logger
        return cls

    @classmethod
    def __fetch_bashrc_line(cls, shell_file="~/.bashrc") -> str:
        """
        Generator that fetches bashrc lines one by one
        """
        _, shell_file = cls.get_shell(shell_file)

        with open(os.path.expanduser(shell_file), "r") as f:
            line = True
            while line:
                line = f.readline()
                yield line

    @classmethod
    def get_shell(
            cls, shell: str = "bash", shell_file: str = "~/.bashrc"
    ) -> Tuple[str, str]:
        """
        Get Shell that is used for every access
        :param shell: Shell binary name
        :param shell_file: Shell file path
        :return: shell binary name, shell file path
        """
        if cls.shell_file != "~/.bashrc":
            shell_file = cls.shell_file

        if cls.shell != "bash":
            shell = cls.shell

        return shell, shell_file

    @classmethod
    def unset(cls, key: str, shell_file="~/.bashrc"):
        """
        Unsets variable from environment
        :param shell_file: Custom Shell file path
        :param key: Key of variable

        Can throw PermissionError if bashrc is not accessible
        """
        shell, shell_file = cls.get_shell(shell_file)

        cls.logger.debug(f"Unsetting system variable {key} {shell=} {shell_file=}")

        replacement_lines = []

        for line in cls.__fetch_bashrc_line(shell_file):

            # Way faster than regex
            # Do search without quotes

            if cls.EXPORT_STRING(key, "")[:-2] in line:
                continue

            replacement_lines.append(line)

        with open(os.path.expanduser(shell_file), "w") as f:
            f.writelines(replacement_lines)

        cls.logger.debug(f"Finished Unsetting system variable {key}")

    @classmethod
    def get(
            cls,
            key: str,
            default: Union[Any, VarNotFound] = VarNotFound,
            shell="bash",
            shell_file="~/.bashrc",
    ) -> str:
        """
        Get Environment Variable
        :param shell: Custom Shell
        :param shell_file: Custom shell file path
        :param key: Key of variable
        :param default: Returned if variable empty or undefined
        :return:
        """
        shell, shell_file = cls.get_shell(shell, shell_file)

        cls.logger.debug(f"Getting variable {key} {shell=} {shell_file}")
        value: str = subprocess.check_output(
            ["/usr/bin/env", shell, "-ic", f". {shell_file} && echo -n ${key}"],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8")

        # Check for empty or unset variable
        if not value:

            if default == VarNotFound:
                cls.logger.debug(f"Variable {key} not found")
                raise VarNotFound("System Variable is empty or undefined")

            cls.logger.debug(f"Returning default variable {key} not found or empty")
            return default

        cls.logger.debug(f"Got variable {key} {value=} {shell=} {shell_file}")
        return value

    @classmethod
    def set(cls, key: str, value: str, shell_file="~/.bashrc"):
        """
        Set Environment Variable
        :param shell_file: Custom Shell File Path
        :param key: Key of variable
        :param value: Value to be set
        """
        shell, shell_file = cls.get_shell(shell_file)

        os.system(f"echo '{cls.EXPORT_STRING(key, value)}' >> {shell_file}")
        cls.logger.debug(f"Set variable {key} {value=} {shell=} {shell_file}")

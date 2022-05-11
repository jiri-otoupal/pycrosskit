#! python3  # noqa: E265

# -- IMPORTS

# standard
import logging
import os

# conditional
if os.name == "nt":
    from pycrosskit.env_platforms.windows import WinVar

    detected_env = WinVar()
else:
    from pycrosskit.env_platforms.linux import LinVar

    detected_env = LinVar()

# -- CLASSES
class SysEnv:
    logger = logging.getLogger("env_vars")
    stdout = logger.info
    stderr = logger.error

    system_env_handler = None

    @classmethod
    def save_shell_specs(cls, shell, shell_file):
        """
        Save state of shell specs for overriding this in all argument functions such as

            shell="bash"
            shell_file="~/.bashrc"

        If specs are saved,
            custom arguments in functions are ignored and replaced with saved

        :param shell:
        :param shell_file:
        """
        if cls.system_env_handler.shell == "batch":
            cls.logger.warning("Trying to change shell of windows machine")

        cls.system_env_handler.shell = shell
        cls.system_env_handler.shell_file = shell_file

    def __new__(cls, *args, **kwargs):
        if cls.system_env_handler is not None:
            cls.logger.debug(f"Accessed instance of type {os.name}")
            return cls.system_env_handler

        cls.logger.debug(f"Created new instance of type {os.name}")
        cls.system_env_handler = detected_env

        return detected_env

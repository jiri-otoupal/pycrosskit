import logging
import os
import sys


class SysEnv(type):
    logger = logging.getLogger("env_vars")
    sys.stdout.write = logger.info
    sys.stderr.write = logger.error

    system_env_handler = None

    def __new__(mcs, *args, **kwargs):
        if mcs.system_env_handler is not None:
            mcs.logger.debug(f"Accessed instance of type {os.name}")
            return mcs.system_env_handler

        if os.name == "nt":
            from pycrosskit.env_platforms.winvar import WinVar

            detected_env = WinVar()
        else:
            from pycrosskit.env_platforms.linvar import LinVar

            detected_env = LinVar()

        mcs.logger.debug(f"Created new instance of type {os.name}")
        mcs.system_env_handler = detected_env

        return detected_env

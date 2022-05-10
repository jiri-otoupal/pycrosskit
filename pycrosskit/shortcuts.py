import os
from collections import namedtuple
from typing import Tuple

UserFolders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))


class Shortcut:
    def __init__(
        self,
        shortcut_name: str,
        exec_path: str,
        description: str = "",
        icon_path: str = "",
        desktop: bool = False,
        start_menu: bool = False,
        work_dir: str = None,
    ):
        """Initialize a shortcut object.

        :param str shortcut_name: Name of Shortcut that will be created
        :param str exec_path: Path to Executable
        :param str description: Custom Description, defaults to ""
        :param str icon_path: Path to icon .ico, defaults to ""
        :param bool desktop: True to Generate Desktop Shortcut, defaults to False
        :param bool start_menu: True to Generate Start Menu Shortcut, defaults to False
        :param str work_dir: _description_, defaults to None
        
        """
        self.exec_path = str(exec_path)
        self.arguments = "".join(exec_path.split(" ")[1:])
        self.shortcut_name = shortcut_name
        self.description = description
        self.icon_path = str(icon_path)
        self.work_path = str(work_dir)
        if os.name == "nt":
            from pycrosskit.shortcut_platforms.windows import create_shortcut
        else:
            from pycrosskit.shortcut_platforms.linux import create_shortcut
        self.desktop_path, self.startmenu_path = create_shortcut(
            self, start_menu, desktop
        )

    @staticmethod
    def delete(
        shortcut_name: str, desktop: bool = False, start_menu: bool = False
    ) -> Tuple[str, str]:
        """Remove existing Shortcut from the system.

        :param str shortcut_name: Name of shortcut
        :param bool desktop: Delete Shortcut on Desktop
        :param bool start_menu: Delete Shortcut on Start Menu

        :return: desktop and startmenu path
        :return Tuple[str, str]: desktop_path, startmenu_path
        """
        if os.name == "nt":
            from pycrosskit.shortcut_platforms.windows import delete_shortcut
        else:
            from pycrosskit.shortcut_platforms.linux import delete_shortcut
        return delete_shortcut(shortcut_name, desktop, start_menu)

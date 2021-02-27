import os
import sys
from collections import namedtuple

UserFolders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))


class Shortcut:

    def __init__(self, shortcut_name: str, exec_path: str, description: str = "", icon_path: str = "",
                 desktop: bool = False,
                 start_menu: bool = False):
        self.exec_path = exec_path
        self.arguments = "".join(exec_path.split(" ")[1:])
        self.shortcut_name = shortcut_name
        self.description = description
        self.icon_path = icon_path
        if not self.get_platform(True):
            from pycrosskit.platforms.windows import create_shortcut
        else:
            from pycrosskit.platforms.linux import create_shortcut
        self.desktop_path, self.startmenu_path = create_shortcut(self, start_menu, desktop)

    @staticmethod
    def delete(shortcut_name, desktop: bool = False, start_menu: bool = False):
        if not Shortcut.get_platform(True):
            from pycrosskit.platforms.windows import delete_shortcut
        else:
            from pycrosskit.platforms.linux import delete_shortcut
        return delete_shortcut(shortcut_name, desktop, start_menu)

    @staticmethod
    def get_platform(boolean: bool = False) -> str or bool:
        """
        Returns current Platform
        :param boolean: Get system in boolean ( Linux is True, Windows is False )
        """
        platform = sys.platform
        if os.name == "nt":
            platform = "win"
        if platform == "linux2":
            platform = "linux"
        if boolean:
            return platform == "linux"
        else:
            return platform

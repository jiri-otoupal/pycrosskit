import os
import sys
from collections import namedtuple

UserFolders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))


class Shortcut:

    def __init__(self, shortcut_name, exec_path, description="",
                 icon_path="",
                 desktop=False,
                 start_menu=False, work_dir=None):
        """

        :param shortcut_name: Name of Shortcut that will be created
        :param exec_path: Path to Executable
        :param description: Custom Description
        :param icon_path: Path to icon .ico
        :param desktop: True to Generate Desktop Shortcut
        :param start_menu: True to Generate Start Menu Shortcut
        """
        self.exec_path = str(exec_path)
        self.arguments = "".join(exec_path.split(" ")[1:])
        self.shortcut_name = shortcut_name
        self.description = description
        self.icon_path = str(icon_path)
        self.work_path = str(work_dir)
        if not self.get_platform(True):
            from pycrosskit.platforms.windows import create_shortcut
        else:
            from pycrosskit.platforms.linux import create_shortcut
        self.desktop_path, self.startmenu_path = create_shortcut(self, start_menu, desktop)

    @staticmethod
    def delete(shortcut_name, desktop=False, start_menu=False):
        """
        Delete Shortcut
        :param shortcut_name: Name of shortcut
        :param desktop: Delete Shortcut on Desktop
        :param start_menu: Delete Shortcut on Start Menu
        :return: desktop and startmenu path
        :rtype: str, str
        """
        if not Shortcut.get_platform(True):
            from pycrosskit.platforms.windows import delete_shortcut
        else:
            from pycrosskit.platforms.linux import delete_shortcut
        return delete_shortcut(shortcut_name, desktop, start_menu)

    @staticmethod
    def get_platform(is_linux=False):
        """
        Returns current Platform
        :param is_linux: Get system in boolean ( Linux is True, Windows is False )
        :return platform as string or bool
        :rtype str or bool
        """
        platform = sys.platform
        if os.name == "nt":
            platform = "win"
        if platform == "linux2":
            platform = "linux"
        if is_linux:
            return platform == "linux"
        else:
            return platform

#! python3  # noqa: E265

# -- IMPORTS

# standard
import os
from collections import namedtuple

# conditional
if os.name == "nt":
    from pycrosskit.shortcut_platforms.windows import (create_shortcut,
                                                       delete_shortcut)
else:
    from pycrosskit.shortcut_platforms.linux import (create_shortcut,
                                                     delete_shortcut)

# -- GLOBALS
UserFolders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))

# -- CLASSES
class Shortcut:
    def __init__(
        self,
        shortcut_name,
        exec_path,
        description="",
        icon_path="",
        desktop=False,
        start_menu=False,
        work_dir=None,
    ):
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

        # create shortcut
        self.desktop_path, self.startmenu_path = create_shortcut(
            self, start_menu, desktop
        )

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
        return delete_shortcut(shortcut_name, desktop, start_menu)

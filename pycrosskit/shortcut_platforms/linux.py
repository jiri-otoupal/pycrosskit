#!/usr/bin/env python
"""
Create desktop shortcuts for Linux
"""
import os
import stat
from pathlib import Path
from typing import Tuple

from pycrosskit.shortcuts import UserFolders, Shortcut

scut_ext = ".desktop"
ico_ext = ("ico", "svg", "png")

DESKTOP_FORM = """[Desktop Entry]
Version=1.0
Name={name:s}
Type=Application
Comment={desc:s}
Icon={icon:s}
Terminal=false
Exec={exe:s} {args:s}
"""

_HOME = None


def get_homedir() -> str:
    """Determine home directory of current user.

    :return str: path to the user home
    """
    global _HOME
    if _HOME is not None:
        return _HOME

    home = None
    try:
        home = str(Path.home())
    except:
        pass

    if home is None:
        home = os.path.expanduser("~")
    if home is None:
        home = os.environ.get("HOME", os.path.abspath(".."))
    _HOME = home
    return home


def get_desktop() -> str:
    """Return the user Desktop folder.

    :return str: path to the Desktop folder
    """
    homedir = get_homedir()
    desktop = os.path.join(homedir, "Desktop")

    # search for .config/user-dirs.dirs in HOMEDIR
    ud_file = os.path.join(homedir, ".config", "user-dirs.dirs")
    if os.path.exists(ud_file):
        val = desktop
        with open(ud_file, "r") as fh:
            text = fh.readlines()
        for line in text:
            if "DESKTOP" in line:
                line = line.replace("$HOME", homedir)[:-1]
                key, val = line.split("=")
                val = val.replace('"', "").replace("'", "")
        desktop = val
    return desktop


def get_startmenu() -> str:
    """Get user start menu location.

    :return str: path to the start menu
    """
    homedir = get_homedir()
    return os.path.join(homedir, ".local", "share", "applications")


def get_folders() -> UserFolders:
    """Get user folders.

    :return UserFolders: user folders named tuple
    """
    return UserFolders(get_homedir(), get_desktop(), get_startmenu())


def create_shortcut(
    shortcut_instance: Shortcut, desktop: bool = False, startmenu: bool = False
):
    """Creates shortcut on the system.

    :param Shortcut shortcut_instance: Shortcut Object
    :param bool startmenu: True to create Start Menu Shortcut
    :param bool desktop: True to create Desktop Shortcut

    :return: desktop and startmenu path
    :rtype: Tuple[str, str]
    """
    if shortcut_instance.work_path is None:
        file_content = DESKTOP_FORM.format(
            name=shortcut_instance.shortcut_name,
            desc=shortcut_instance.description,
            exe=shortcut_instance.exec_path,
            icon=shortcut_instance.icon_path,
            args=shortcut_instance.arguments,
        )
    else:
        file_content = DESKTOP_FORM.format(
            name=shortcut_instance.shortcut_name,
            desc=shortcut_instance.description,
            exe=f"bash -c "
            f"'cd {shortcut_instance.work_path}"
            f" && {shortcut_instance.exec_path}'",
            icon=shortcut_instance.icon_path,
            args=shortcut_instance.arguments,
        )
    user_folders = get_folders()
    desktop_path = Path(user_folders.desktop)
    startmenu_path = Path(user_folders.startmenu)

    if desktop:
        __write_shortcut(desktop_path, shortcut_instance, file_content)

    if startmenu:
        __write_shortcut(startmenu_path, shortcut_instance, file_content)

    return desktop_path, startmenu_path


def delete_shortcut(shortcut_name, desktop: bool = False, startmenu: bool = False):
    """Remove shortcut from the system.

    :param str shortcut_name: Shortcut Object
    :param bool startmenu: True to create Start Menu Shortcut, defaults to False
    :param bool desktop: True to create Desktop Shortcut, defaults to False

    :return Tuple[str, str]: desktop_path, startmenu_path
    """
    user_folders = get_folders()
    desktop_path, startmenu_path = "", ""
    if startmenu:
        startmenu_path = user_folders.startmenu + "/" + shortcut_name + scut_ext
        if os.path.exists(startmenu_path):
            os.chmod(startmenu_path, stat.S_IWRITE)
            os.remove(startmenu_path)
    if desktop:
        desktop_path = user_folders.desktop + "/" + shortcut_name + scut_ext
        if os.path.exists(desktop_path):
            os.chmod(desktop_path, stat.S_IWRITE)
            os.remove(desktop_path)
    return desktop_path, startmenu_path


def __write_shortcut(dest_path: Path, shortcut_instance: str, file_content: str):
    """Writes shortcut content to destination.

    :param Path dest_path: Path where write file
    :param str shortcut_instance: Instance of shortcut that will be used
    :param str file_content: Content of future icon from DESKTOP_FORM.format(...)
    """
    if not dest_path.parent.exists():
        os.makedirs(str(dest_path))
    dest = str(dest_path / (shortcut_instance.shortcut_name + scut_ext))
    with open(dest, "w") as f_out:
        f_out.write(file_content)
    st = os.stat(dest)
    os.chmod(dest, st.st_mode | stat.S_IEXEC)

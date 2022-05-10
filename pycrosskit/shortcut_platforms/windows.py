#!/usr/bin/env python
"""
Create desktop shortcuts for Windows
"""
import os
import stat
from pathlib import Path
from typing import Tuple

import win32com.client
from win32comext.shell import shell, shellcon

from pycrosskit.shortcuts import UserFolders, Shortcut

scut_ext = '.lnk'
ico_ext = ('ico',)

# batch file to activate the environment
# for Anaconda Python before running command.


_WSHELL = win32com.client.Dispatch("Wscript.Shell")


# Windows Special Folders
# see: https://docs.microsoft.com/en-us/windows/win32/shell/csidl

def get_homedir() -> str:
    """Return home directory.
    
    Note that we return CSIDL_PROFILE, not CSIDL_APPDATA, 
    CSIDL_LOCAL_APPDATA,  or CSIDL_COMMON_APPDATA.

    :return str: path to the user home
    """
    return shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, None, 0)


def get_desktop() -> str:
    """Return the user Desktop folder.
    
    :return str: path to the Desktop folder
    """
    return shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)


def get_startmenu() -> str:
    """Return user Start Menu Programs folder.

    Note that we return CSIDL_PROGRAMS not CSIDL_COMMON_PROGRAMS

    :return str: path to the Start Menu Programs folder
    """
    return shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAMS, None, 0)


def get_folders() -> UserFolders:
    """Get user folders.

    :return UserFolders: user folders named tuple
    """    
    return UserFolders(get_homedir(), get_desktop(), get_startmenu())


def create_shortcut(shortcut_instance: Shortcut, startmenu: bool=False, desktop: bool=False) -> Tuple[str, str]:
    """Creates shortcut on the system.

    :param Shortcut shortcut_instance: Shortcut Object
    :param bool startmenu: True to create Start Menu Shortcut
    :param bool desktop: True to create Desktop Shortcut

    :return: desktop and startmenu path
    :rtype: Tuple[str, str]
    """
    user_folders = get_folders()
    desktop_path, startmenu_path = None, None

    if startmenu:
        startmenu_path = str(Path(user_folders.startmenu) / (shortcut_instance.shortcut_name + scut_ext))
        _wscript_shortcut(startmenu_path, shortcut_instance)
    if desktop:
        desktop_path = str(Path(user_folders.desktop) / (shortcut_instance.shortcut_name + scut_ext))
        _wscript_shortcut(desktop_path, shortcut_instance)
    return desktop_path, startmenu_path


def delete_shortcut(shortcut_name: str, startmenu: bool=False, desktop: bool=False) -> Tuple[str, str]:
    """Remove shortcut from the system.

    :param str shortcut_name: Shortcut Object
    :param bool startmenu: True to create Start Menu Shortcut, defaults to False
    :param bool desktop: True to create Desktop Shortcut, defaults to False

    :return Tuple[str, str]: desktop_path, startmenu_path
    """
    user_folders = get_folders()
    desktop_path, startmenu_path = "", ""
    if startmenu:
        startmenu_path = str(Path(user_folders.startmenu) / (shortcut_name + scut_ext))
        if os.path.exists(startmenu_path):
            os.chmod(startmenu_path, stat.S_IWRITE)
            os.remove(startmenu_path)
    if desktop:
        desktop_path = str(Path(user_folders.desktop) / (shortcut_name + scut_ext))
        if os.path.exists(desktop_path):
            os.chmod(desktop_path, stat.S_IWRITE)
            os.remove(desktop_path)
    return desktop_path, startmenu_path


def _wscript_shortcut(dest_path: str, shortcut_instance: Shortcut) -> None:
    """Shortcut secondary function.

    :param dest_path: Destination path for shortcut
    :param shortcut_instance: Shortcut instance
    """
    wscript = _WSHELL.CreateShortCut(dest_path)
    wscript.Targetpath = shortcut_instance.exec_path
    wscript.Arguments = shortcut_instance.arguments
    if shortcut_instance.work_path is not None:
        wscript.WorkingDirectory = shortcut_instance.work_path
    wscript.WindowStyle = 0
    wscript.Description = shortcut_instance.description
    if os.path.exists(shortcut_instance.icon_path):
        wscript.IconLocation = shortcut_instance.icon_path
    wscript.save()

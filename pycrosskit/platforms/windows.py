#!/usr/bin/env python
"""
Create desktop shortcuts for Windows
"""
import os
import stat

import win32com.client
from win32comext.shell import shell, shellcon

from pycrosskit.shortcuts import UserFolders

scut_ext = '.lnk'
ico_ext = ('ico',)

# batch file to activate the environment
# for Anaconda Python before running command.


_WSHELL = win32com.client.Dispatch("Wscript.Shell")


# Windows Special Folders
# see: https://docs.microsoft.com/en-us/windows/win32/shell/csidl

def get_homedir():
    '''Return home directory:
    note that we return CSIDL_PROFILE, not
    CSIDL_APPDATA, CSIDL_LOCAL_APPDATA,  or CSIDL_COMMON_APPDATA
    '''
    return shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, None, 0)


def get_desktop():
    '''Return user Desktop folder'''
    return shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)


def get_startmenu():
    '''Return user Start Menu Programs folder
    note that we return CSIDL_PROGRAMS not CSIDL_COMMON_PROGRAMS
    '''
    return shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAMS, None, 0)


def get_folders():
    return UserFolders(get_homedir(), get_desktop(), get_startmenu())


def create_shortcut(shortcut_instance, startmenu=False, desktop=False):
    """
    Creates Shortcut
    :param shortcut_instance: Shortcut Object
    :param startmenu: True to create Start Menu Shortcut
    :param desktop: True to create Desktop Shortcut
    :return desktop_path, startmenu_path
    :rtype: str, str
    """
    user_folders = get_folders()
    desktop_path, startmenu_path = None, None

    if startmenu:
        startmenu_path = user_folders.startmenu + "/" + shortcut_instance.shortcut_name + scut_ext
        _wscript_shortcut(startmenu_path, shortcut_instance,
                          user_folders)
    if desktop:
        desktop_path = user_folders.desktop + "/" + shortcut_instance.shortcut_name + scut_ext
        _wscript_shortcut(desktop_path, shortcut_instance,
                          user_folders)
    return desktop_path, startmenu_path


def delete_shortcut(shortcut_name, startmenu=False, desktop=False):
    """
    Deletes Shortcut
    :param shortcut_name: Shortcut Object
    :param startmenu: True to create Start Menu Shortcut
    :param desktop: True to create Desktop Shortcut
    :return desktop_path, startmenu_path
    :rtype: str, str
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


def _wscript_shortcut(dest_path, shortcut_instance, user_folders):
    """
    Shortcut secondary function
    :param dest_path: Destination path for shortcut
    :param shortcut_instance: Shortcut instance
    :param user_folders: System folders
    """
    wscript = _WSHELL.CreateShortCut(dest_path)
    wscript.Targetpath = shortcut_instance.exec_path
    wscript.Arguments = shortcut_instance.arguments
    wscript.WorkingDirectory = user_folders.home
    wscript.WindowStyle = 0
    wscript.Description = shortcut_instance.description
    if os.path.exists(shortcut_instance.icon_path):
        wscript.IconLocation = shortcut_instance.icon_path
    wscript.save()

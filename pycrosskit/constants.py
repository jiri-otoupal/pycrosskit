from collections import namedtuple

user_folders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))
"""
Regex Pattern Splits executable and arguments using the space
immediately after file extension as seperator
"""
parse_arguments_pattern = r'"?([^.]*[.][^ "]*)"? ?(.*)'

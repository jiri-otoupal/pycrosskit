from collections import namedtuple

UserFolders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))
ParseArgumentsPattern = r'"?([^.]*[.][^ "]*)"? ?(.*)'  # Splits executable and arguments using the space immediately after file extension as seperator

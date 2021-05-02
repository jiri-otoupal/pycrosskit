"""
pycrosskit
~~~~~~

The pycrosskit package - a Python package that makes Shortcuts and Environment Variables Easy
"""

# Shortcuts usage:


# Will Create shortcut
# * at Desktop if desktop is True
# * at Start Menu if start_menu is True
#
#   Shortcut(shortcut_name, exec_path, description,
#         icon_path, desktop, start_menu)
#
## Will Delete shortcut
## * at Desktop if desktop is True
## * at Start Menu if start_menu is True
#   Shortcut.delete(shortcut_name, desktop, start_menu)
#
#
#
##### Environment Variables usage:
#
#
## Will Set Persistent Value for Variable in System
## * subkey works only for windows like file in folder
## * reg_path works only for windows as register path
#   SysEnv.set_var(name, value, subkey, reg_path=default_reg_path)

## Will Get Persistent Value for Variable in System
## * reg_path works only for windows as register path
## * delete, deletes key from environment and its subkeys after read
#   SysEnv.get_var(name, reg_path=default_reg_path, delete=False)

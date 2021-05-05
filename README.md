# Python Cross Platform Toolkit for Windows and Linux variables, shortcuts and start menu shortcuts

## Simple Cross Platform creation of shortcuts and Persistent Environment Variables

[![image](https://img.shields.io/pypi/v/pycrosskit.svg)](https://pypi.org/project/py-cross-kit/)
[![Build Status](https://travis-ci.com/jiri-otoupal/pycrosskit.svg?branch=master)](https://travis-ci.com/github/jiri-otoupal/pycrosskit)
[![Downloads](https://pepy.tech/badge/pycrosskit)](https://pepy.tech/project/pycrosskit)

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
pip install pycrosskit

or

pip3 install pycrosskit
```

#### Supported Platforms:

* Linux
* Windows

#### Shortcuts usage:

```python
# Will Create shortcut 
# * at Desktop if desktop is True 
# * at Start Menu if start_menu is True

Shortcut(shortcut_name, exec_path, description,
         icon_path, desktop, start_menu)

# Will Delete shortcut
# * at Desktop if desktop is True 
# * at Start Menu if start_menu is True
Shortcut.delete(shortcut_name, desktop, start_menu)

```

#### Environment Variables usage:

```python
# Will Set Persistent Value for Variable in System
# * subkey works only for windows like file in folder
# * reg_path works only for windows as register path 
SysEnv.set_var(name, value, subkey, reg_path=default_reg_path)

# Will Get Persistent Value for Variable in System
# * reg_path works only for windows as register path
# * delete, deletes key from environment and its subkeys after read
SysEnv.get_var(name, reg_path=default_reg_path, delete=False)


```
<hr>
Did I make your life less painfull ? 
<br>
<br>
Support my coffee addiction ;)
<br>
<a href="https://www.buymeacoffee.com/jiriotoupal" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy me a Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

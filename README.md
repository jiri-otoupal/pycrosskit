# Python Cross Platform Toolkit for Windows and Linux variables, shortcuts and start menu shortcuts

Simple Cross Platform creation of shortcuts and Persistent Environment Variables

[![image](https://img.shields.io/pypi/v/pycrosskit.svg)](https://pypi.org/project/pycrosskit/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pycrosskit)](https://pypi.org/project/pycrosskit/)

[![Build Status](https://travis-ci.com/jiri-otoupal/pycrosskit.svg?branch=master)](https://travis-ci.com/github/jiri-otoupal/pycrosskit)
[![Downloads](https://pepy.tech/badge/pycrosskit)](https://pepy.tech/project/pycrosskit)

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
pip install pycrosskit

or

pip3 install pycrosskit
```

## Supported Platforms:

* Linux
* Windows

## Shortcuts usage:

```python
from pycrosskit.shortcuts import Shortcut

# Will Create shortcut 
# * at Desktop if desktop is True 
# * at Start Menu if start_menu is True

Shortcut(shortcut_name="My Spaghetti Shortcut", exec_path="/usr/bin/order_spaghetti", description="Such Yummy Spaghetti",
         icon_path="/home/.../spaghetti.png", desktop=True, start_menu=True)

# Will Delete shortcut
# * at Desktop if desktop is True 
# * at Start Menu if start_menu is True
Shortcut.delete(shortcut_name="My Spaghetti Shortcut", desktop=True, start_menu=True)

```

## Environment Variables usage:

Accessing and write to environment variables is automatically handled based on your system Lin/Win SysEnv class is
implemented as a singleton metaclass so don't be afraid about multiple instances

**Support of Mac env variables on request**

```python
from pycrosskit.envariables import SysEnv

### ** Linux ** 

# Will Set Persistent Value for Variable in Systems bashrc file or custom one that you can pass
SysEnv().set(key="spaghetti", value="boloneys", shell_file="~/.zsh")

# Will Get Persistent Value for Variable in System
# * reg_path works only for windows as register path
# * registry works only for windows, if is False variable is obtained from User Environment Variables
SysEnv().get(key="spaghetti", shell_file="~/.zsh", shell="zsh")

# Will unset variable from your environment or registry
SysEnv().unset(key="spaghetti", shell_file="~/.zsh")

# For not having to override argument shell_file or shell
# This saves specs for every access, default arguments are ignored
SysEnv.save_shell_specs(shell="zsh", shell_file="~/.zsh")

### ** Windows **

# Will Set Persistent Value for Variable in System
# * subkey works only for windows like file in folder
# * reg_path works only for windows as register path (is ignored if registry=False) 
# * registry works only for windows, if is False variable is saved to User Environment Variables
SysEnv().set(key="spaghetti", value="bologna", subkey="italian_food", reg_path="HKEY-...\\CustomPath",
             registry=True)

# Will Get Persistent Value for Variable in System
# * reg_path works only for windows as register path
# * registry works only for windows, if is False variable is obtained from User Environment Variables
SysEnv().get(key="spaghetti", reg_path="HKEY-...\\CustomPath", registry=True)

# Will unset variable from your environment or registry
SysEnv().unset(key="spaghetti", registry=True)
```

## Develop

Clone the repository, then:

```sh
# install dependencies and package in editable mode
python -m pip install -U -r requirements.txt
# install development dependencies
python -m pip install -U -e .[dev]
```

----

<hr>
Did I made your life less painfull ? 
<br>
<br>
Support my coffee addiction ;)
<br>
<a href="https://www.buymeacoffee.com/jiriotoupal" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy me a Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

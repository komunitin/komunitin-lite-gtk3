# Komunitin Lite

Basic python GTK3 client for komunitin users.

![Workflow status](https://github.com/XaviP/komunitin-lite-gtk3/workflows/Python_app/badge.svg)


**Note: The development of this project is stopped to focus on [Komunitin Lite Qt](https://github.com/komunitin/komunitin_lite_qt), because we think that Qt is a better option for a cross-platform client. This repository remains alive as a form of documentation for the use of the komunitin API rest.**


### System dependencies

All dependencies are already installed by default in most current GNU/Linux distributions:
- python >= 3.7 (with requests, threading, etc...)
- PyGObject >= 3.36.0

(if not try: `sudo apt install python3 python3-gi python3-requests`)


### Installation

To run:

    git clone https://github.com/XaviP/komunitin-lite-gtk3.git
    cd komunitin-lite-gtk3
    ./run_komunitin_lite

You can choose your configuration (server) by copying the config_default.ini file: 

    `cp komunitin_lite/config_default.ini komunitin_lite/config.ini`

and edit the `komunitin_lite/config.ini` file.

To install:

    pip3 install --user .

You can launch the app from the desktop. 

To uninstall:

    pip3 uninstall komunitin_lite

To run tests: `python3 -m unittest`

You can develop another UI with the core. See [core/README.md](https://github.com/XaviP/komunitin-lite-gtk3/blob/master/komunitin_lite/core/README.md).


#### TODO
- Transfers pagination
- Update translations
- More tests
- ... 


# Komunitin Lite

Basic python GTK3 client for komunitin users.

![Workflow status](https://github.com/XaviP/komunitin-lite-gtk3/workflows/Python_app/badge.svg)

All dependencies are already installed by default in most current GNU/Linux distributions:
- python >= 3.7 (with requests, threading, etc...)
- PyGObject >= 3.36.0

You can choose your configuration (server) by copying the config_default.ini file: 

    `cp komunitin_lite/config_default.ini komunitin_lite/config.ini`

and edit the `komunitin_lite/config.ini` file.


### Installation

To run:

    git clone https://github.com/XaviP/komunitin-lite-gtk3.git
    cd komunitin-lite-gtk3
    ./run_komunitin_lite

To install:

    pip3 install --user .

You can launch the app from the desktop. 

To uninstall:

    pip3 uninstall komunitin_lite

Comming soon: deb package and ppa

To run tests: `python3 -m unittest`

You can develop another UI with the core. See [core/README.md](https://github.com/XaviP/komunitin-lite-gtk3/blob/master/komunitin_lite/core/README.md).


#### TODO
- Transfers pagination
- Finish and test make transactions
- Update translations
- More tests
- ... 


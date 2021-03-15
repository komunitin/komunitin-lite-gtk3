# Komunitin Lite

Basic python GTK3 client for komunitin users.

![Workflow status](https://github.com/XaviP/komunitin-lite-gtk3/workflows/Python_app/badge.svg)

All dependencies are already installed by default in most current GNU/Linux distributions:
- python >= 3.8 (requests, threading, etc...)
- PyGObject >= 3.36.0

You can choose your configuration (server) by copying the config_default.ini file: 

    `cp config_default.ini config.ini`

and edit the `config.ini` file.


To run `python3 komunitin`

(or `python3 komunitin --cli` for command line interface)


To run tests: `python3 -m unittest`


You can develop another UI with the core. See README in core/


#### TODO
- Transfers pagination
- Finish and test make transactions
- Update translations
- More tests
- ... 


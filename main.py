#!/usr/bin/env python3
import asyncio
import logging
import sys

import typing
import zmq

import collectors_handler
import proxies_handler
import results_handler
import server
import settings
import tasks_handler


def main() -> int:
    init_logging()

    if len(sys.argv) < 2:
        print("Command is required")
        print()
        print_help()
        return 1

    command = sys.argv[1].strip().lower().replace("_", "-")
    sys.argv = sys.argv[1:]
    try:
        func: typing.Any = {
            "collectors-handler": collectors_handler.main,
            "proxies-handler": proxies_handler.main,
            "tasks-handler": tasks_handler.main,
            "results-handler": results_handler.main,
            "server": server.main,
            "print-version": print_version,
            "version": print_version,
            "--version": print_version,
            "-v": print_version,
        }[command]

        if asyncio.iscoroutinefunction(func):
            return asyncio.run(func())

        return func()
    except KeyError:
        print("Unknown command")
        print_help()
        return 2


help_message = """Usage: ./main.py COMMAND [OPTION]...
Runs proxy_py

The commands are:
// TODO: update
    "core" - runs core part of the project (proxies parsing and processing)
    "print_collectors" - prints collectors
    "server" - runs server for providing API

use ./main.py COMMAND --help to get more information

Project's page: https://github.com/DevAlone/proxy_py
"""


def print_help():
    print(help_message)


def print_version():
    print(f"libzmq version is\t{zmq.zmq_version()}")
    print(f"pyzmq version is\t{zmq.__version__}")


def init_logging():
    logging.root.setLevel(settings.log_level)
    formatter = logging.Formatter(settings.log_format)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)


if __name__ == "__main__":
    exit(main())

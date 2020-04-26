#!/usr/bin/env python3
import asyncio
import logging
import sys

import zmq

import broker
import proxies_handler
import results_handler
import settings
import tasks_handler


async def main() -> int:
    init_logging()

    if len(sys.argv) < 2:
        print("Command is required")
        print()
        await print_help()
        return 1

    command = sys.argv[1].strip().lower()
    sys.argv = sys.argv[1:]
    try:
        func = {
            "proxies_handler": proxies_handler.main,
            "tasks_handler": tasks_handler.main,
            "broker": broker.main,
            "results_handler": results_handler.main,
            "print_version": print_version,
            "version": print_version,
            "--version": print_version,
            "-v": print_version,
        }[command]

        return await func()
    except KeyError:
        print("Unknown command")
        await print_help()
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


async def print_help():
    print(help_message)


async def print_version():
    print(f"libzmq version is\t{zmq.zmq_version()}")
    print(f"pyzmq version is\t{zmq.__version__}")


def init_logging():
    logging.root.setLevel(settings.log_level)


if __name__ == "__main__":
    exit(asyncio.run(main()))

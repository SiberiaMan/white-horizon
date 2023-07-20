#!/usr/bin/env python

import argparse
import logging
import logging.config
import os
import sys

import pytest
from aiohttp import web

APP_NAME = "app"


def run(args=None):
    from app.app import create_app

    host = args.host if args else os.environ.get("HOST", "0.0.0.0")
    port = args.port if args else os.environ.get("PORT", 5000)
    log_level = args.log_level if args else "INFO"

    app = create_app()

    if "logging_config" in app["config"]:
        logging.config.dictConfig(app["config"]["logging_config"])
    else:
        logging.basicConfig(level=log_level)

    web.run_app(app, host=host, port=port)


def test():
    def stub(text):
        pass

    save_out_write = sys.stdout.write
    sys.stdout.write = stub

    save_err_write = sys.stderr.write
    sys.stderr.write = stub

    ret = pytest.main(["--junitxml=unittest_report.xml", "storage"])

    sys.stdout.write = save_out_write
    sys.stderr.write = save_err_write

    if args.print:
        with open("unittest_report.xml") as f:
            print(f.read())
    return ret


def print_version():
    from importlib import import_module

    pkg = import_module(APP_NAME, package=".")
    print(pkg.__version__)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Methods management entrypoint")
    subparsers = parser.add_subparsers(dest="command", help="List commands")

    run_project_parser = subparsers.add_parser("run", help="Run")
    run_project_parser.add_argument("--host", dest="host", help="Run on host")
    run_project_parser.add_argument("--port", dest="port", help="Run on port")
    run_project_parser.add_argument("--log_level", dest="log_level", help="Log level")

    test_parser = subparsers.add_parser("test", help="Run test")
    test_parser.add_argument(
        "--print", action="store_true", dest="print", help="Print report"
    )

    subparsers.add_parser("print_version", help="Print application version")

    args = parser.parse_args()
    if args.command == "run":
        sys.exit(run(args))

    if args.command == "test":
        sys.exit(test())

    if args.command == "print_version":
        sys.exit(print_version())

    sys.exit(run())

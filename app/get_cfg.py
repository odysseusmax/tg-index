#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import exit
import os


def get_config(name: str, default_value=None, should_prompt=False, error_message=None):
    val = os.environ.get(name, default_value)
    if not val and should_prompt:
        try:
            val = input(f"enter {name}'s value: ")
        except EOFError:
            val = default_value
    if not val and should_prompt:
        print(error_message)
        exit(1)
    print("\n")
    return val

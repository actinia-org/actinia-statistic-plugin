# -*- coding: utf-8 -*-
"""SPDX-FileCopyrightText: (c) 2018-2025 mundialis GmbH & Co. KG

SPDX-License-Identifier: GPL-3.0-or-later

init.
"""
import importlib.metadata

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = importlib.metadata.version(dist_name)
except Exception:
    __version__ = "unknown"

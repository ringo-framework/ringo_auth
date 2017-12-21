#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tedega_auth.server import build_app
application = build_app("tedega_auth")

if __name__ == "__main__":
    application.run()

#!/usr/bin/env python3.4

from digest import app
import setup

app.run(host='0.0.0.0', port=60001, debug=True)

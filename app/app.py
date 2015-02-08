#!/usr/bin/env python2

import os
import sys

from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'Main page.'


@app.route('/pow/<int:x>/<int:y>')
def pow(x, y):
    s = str(x ** y)
    n = 80
    parts = [s[i:i+n] for i in xrange(0, len(s), n)]
    return '\n'.join(parts)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file(sys.argv[1], 'w').write(str(os.getpid()))

    app.run(host='0.0.0.0', port=8000)

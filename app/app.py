#!/usr/bin/env python2

import os

from flask import Flask


app = Flask(__name__)
responder = os.environ['host'] + ':' + os.environ['port']


@app.route('/')
def index():
    return responder


@app.route('/pow/<int:x>/<int:y>')
def pow(x, y):
    s = str(x ** y)
    n = 80
    parts = [s[i:i+n] for i in xrange(0, len(s), n)]
    return responder + '\n' + '\n'.join(parts)


if __name__ == '__main__':
    file(os.environ['pidfile'], 'w').write(str(os.getpid()))
    app.run(host=os.environ['host'], port=int(os.environ['port']))

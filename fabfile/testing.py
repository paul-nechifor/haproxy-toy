from threading import Thread
from urllib2 import Request, urlopen
from time import time


class User(Thread):
    def __init__(self, n_requests):
        super(User, self).__init__()
        self.n_requests = n_requests

    def run(self):
        for _ in xrange(self.n_requests):
            self.make_request()

    def make_request(self):
        request = Request(self.make_request_url())
        start = time()
        text = urlopen(request).read()
        duration = time() - start
        responder = text.split('\n', 1)[0]
        print responder, duration

    def make_request_url(self):
        return 'http://172.17.1.11/pow/2/20000'


class Pounder(object):
    def __init__(self, n_users=1, n_requests=1):
        self.n_users = n_users
        self.n_requests = n_requests

    def start(self):
        users = []
        for _ in xrange(self.n_users):
            user = User(self.n_requests)
            user.start()
            users.append(user)
        for user in users:
            user.join()

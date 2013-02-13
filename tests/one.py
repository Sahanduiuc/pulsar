import time

from pulsar import send, get_actor
from pulsar.apps.test import unittest


class TestOneAsync(unittest.TestCase):
    
    def test_ping_monitor(self):
        worker = get_actor()
        future = yield send('monitor', 'ping')
        self.assertEqual(future, 'pong')
        yield self.async.assertEqual(send(worker.monitor, 'ping'), 'pong')
        response = yield send('monitor', 'notify', worker.info())
        # make sure your last line is a yield if you are waiting for
        # yields as above
        self.assertTrue(response < time.time())
import unittest
from BiblioPixelAnimations.simple import Random


class RandomTest(unittest.TestCase):
    def test_distribution(self):
        d = Random.Distribution()
        expected = {
            'high': 256,
            'low': 0,
            'mode': None,
            'name': 'triangular',
            'scale': 1,
        }
        self.assertEqual(d.vars(), expected)

        N = 100
        for i in range(10):
            mean = sum(d() for i in range(N)) / N
            self.assertGreater(mean, 90)
            self.assertLess(mean, 160)
            # Will fail one time in trillions, is my guess.

        d.name = 'paretovariate'
        expected = {
            'alpha': 1,
            'name': 'paretovariate',
            'scale': 1,
        }
        self.assertEqual(d.vars(), expected)
        values = [d() for i in range(100)]
        self.assertGreater(max(values), 6)
        self.assertLess(min(values), 1.2)

    def test_error(self):
        d = Random.Distribution()
        d.high = d.low

        with self.assertRaises(AttributeError):
            d.sigma
        with self.assertRaises(AttributeError):
            d.mu = 3

        d.name = 'gauss'
        d.mu = d.sigma

        with self.assertRaises(AttributeError):
            d.hi
        with self.assertRaises(AttributeError):
            d.lo = 3

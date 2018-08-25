import random
from bibliopixel.animation import Animation


class Random(Animation):
    """
    Randomly set the color
    """
    def __init__(self, *args, distribution=None, every=0, count=0, levels=None,
                 **kwds):
        super().__init__(*args, **kwds)
        self.distribution = Distribution(**(distribution or {}))
        self.count = count
        self.every = every
        self.levels = levels or [1, 1, 1]

    def step(self, amt=1):
        if not (self.every and self.cur_step % self.every):
            indexes = range(len(self.color_list))
            if self.count:
                indexes = random.sample(indexes, self.count)
            d = self.distribution
            r, g, b = self.levels
            for i in indexes:
                self.color_list[i] = (r * d(), g * d(), b * d())


class Distribution:
    MEMBERS = 'name', 'scale', 'vars'

    def __init__(self, name='triangular', **kwds):
        self.name = name
        for k, v in kwds.items():
            setattr(self, k, v)

    def __call__(self):
        return self.scale * self._function(**self._kwds)

    def __getattribute__(self, key):
        if key.startswith('_') or key in Distribution.MEMBERS:
            return super().__getattribute__(key)
        elif key in self._kwds:
            return self._kwds[key]
        else:
            self._bad_key(key)

    def __setattr__(self, key, value):
        if key.startswith('_') or key in Distribution.MEMBERS:
            super().__setattr__(key, value)
        elif key in self._kwds:
            self._kwds[key] = value
        else:
            self._bad_key(key)

    def _bad_key(self, key):
        params = ', '.join(sorted(self._kwds))
        raise AttributeError(UNKNOWN_FIELD_ERROR % (params, key))

    def __dir__(self):
        return ['name', 'scale'] + list(self._kwds)

    def vars(self):
        return {k: getattr(self, k) for k in dir(self)}

    @property
    def name(self):
        return self._function.__name__

    @name.setter
    def name(self, name):
        dist = _Distribution.get(name)
        self.scale = dist.scale
        self._kwds = dict(dist.kwds)
        self._function = dist.function


class _Distribution:
    DISTRIBUTIONS = {}

    def __init__(self, name, scale, **kwds):
        self.function = getattr(random, name)
        self.scale = scale
        self.kwds = kwds
        self.DISTRIBUTIONS[name] = self

    @classmethod
    def get(cls, name):
        dist = cls.DISTRIBUTIONS.get(name)
        if dist:
            return dist
        else:
            raise ValueError(NOT_DISTRIBUTION_FUNCTION_ERROR % name)


_Distribution('betavariate', 256, alpha=1, beta=1)
_Distribution('expovariate', 256, lambd=0.5)
_Distribution('gauss', 1, mu=128, sigma=32)
_Distribution('lognormvariate', 3, mu=1, sigma=1)
_Distribution('normalvariate', 1, mu=128, sigma=32)
_Distribution('paretovariate', 1, alpha=1)
_Distribution('triangular', 1, low=0, high=256, mode=None)
_Distribution('uniform', 1, a=0, b=256)
_Distribution('vonmisesvariate', 42, mu=1, kappa=1)
_Distribution('weibullvariate', 32, alpha=1, beta=1)

NOT_DISTRIBUTION_FUNCTION_ERROR = """\
Function random.%s is not a distribution
Distribution functions are:
""" + ', '.join(_Distribution.DISTRIBUTIONS)

UNKNOWN_FIELD_ERROR = 'Expected one of function, %s, but got attribute "%s"'

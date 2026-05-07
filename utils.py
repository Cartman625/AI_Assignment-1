"""Provide some widely useful utilities. Safe for "from utils import *".

"""

from __future__ import generators
import operator, math, random, copy, sys, os.path, bisect, inspect


def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" % (method, line, fileName))
    sys.exit(1)


# ______________________________________________________________________________
# Compatibility with Python 2.2 and 2.3

try:
    enumerate  ## Introduced in 2.3
except NameError:
    def enumerate(collection):
        i = 0
        it = iter(collection)
        while 1:
            yield (i, it.next())
            i += 1

try:
    reversed  ## Introduced in 2.4
except NameError:
    def reversed(seq):
        if hasattr(seq, 'keys'):
            raise ValueError("mappings do not support reverse iteration")
        i = len(seq)
        while i > 0:
            i -= 1
            yield seq[i]

try:
    sorted  ## Introduced in 2.4
except NameError:
    def sorted(seq, cmp=None, key=None, reverse=False):
        seq2 = copy.copy(seq)
        if key:
            if cmp == None:
                cmp = __builtins__.cmp
            seq2.sort(lambda x, y: cmp(key(x), key(y)))
        else:
            if cmp == None:
                seq2.sort()
            else:
                seq2.sort(cmp)
        if reverse:
            seq2.reverse()
        return seq2

try:
    set, frozenset
except NameError:
    try:
        import sets
        set, frozenset = sets.Set, sets.ImmutableSet
    except (NameError, ImportError):
        class BaseSet:
            def __init__(self, elements=[]):
                self.dict = {}
                for e in elements:
                    self.dict[e] = 1
            def __len__(self): return len(self.dict)
            def __iter__(self):
                for e in self.dict: yield e
            def __contains__(self, element): return element in self.dict
            def issubset(self, other):
                for e in self.dict.keys():
                    if e not in other: return False
                return True
            def issuperset(self, other):
                for e in other:
                    if e not in self: return False
                return True
            def union(self, other): return type(self)(list(self) + list(other))
            def intersection(self, other): return type(self)([e for e in self.dict if e in other])
            def difference(self, other): return type(self)([e for e in self.dict if e not in other])
            def symmetric_difference(self, other):
                return type(self)([e for e in self.dict if e not in other] +
                                  [e for e in other if e not in self.dict])
            def copy(self): return type(self)(self.dict)
            def __repr__(self):
                elements = ", ".join(map(str, self.dict))
                return "%s([%s])" % (type(self).__name__, elements)
            __le__ = issubset
            __ge__ = issuperset
            __or__ = union
            __and__ = intersection
            __sub__ = difference
            __xor__ = symmetric_difference

        class frozenset(BaseSet):
            def __init__(self, elements=[]):
                BaseSet.__init__(elements)
                self.hash = 0
                for e in self: self.hash |= hash(e)
            def __hash__(self): return self.hash

        class set(BaseSet):
            def update(self, other):
                for e in other: self.add(e)
                return self
            def intersection_update(self, other):
                for e in self.dict.keys():
                    if e not in other: self.remove(e)
                return self
            def difference_update(self, other):
                for e in self.dict.keys():
                    if e in other: self.remove(e)
                return self
            def symmetric_difference_update(self, other):
                to_remove1 = [e for e in self.dict if e in other]
                to_remove2 = [e for e in other if e in self.dict]
                self.difference_update(to_remove1)
                self.difference_update(to_remove2)
                return self
            def add(self, element): self.dict[element] = 1
            def remove(self, element): del self.dict[element]
            def discard(self, element):
                if element in self.dict: del self.dict[element]
            def pop(self):
                key, val = self.dict.popitem()
                return key
            def clear(self): self.dict.clear()
            __ior__ = update
            __iand__ = intersection_update
            __isub__ = difference_update
            __ixor__ = symmetric_difference_update

infinity = 1.0e400

def Dict(**entries): return entries

class DefaultDict(dict):
    def __init__(self, default):
        self.default = default
    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, copy.deepcopy(self.default))
    def __copy__(self):
        copy = DefaultDict(self.default)
        copy.update(self)
        return copy

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    def __cmp__(self, other):
        if isinstance(other, Struct):
            return cmp(self.__dict__, other.__dict__)
        else:
            return cmp(self.__dict__, other)
    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)

def update(x, **entries):
    if isinstance(x, dict): x.update(entries)
    else: x.__dict__.update(entries)
    return x

def removeall(item, seq):
    if isinstance(seq, str): return seq.replace(item, '')
    else: return [x for x in seq if x != item]

def unique(seq): return list(set(seq))

def product(numbers): return reduce(operator.mul, numbers, 1)

def count_if(predicate, seq):
    f = lambda count, x: count + (not not predicate(x))
    return reduce(f, seq, 0)

def find_if(predicate, seq):
    for x in seq:
        if predicate(x): return x
    return None

def every(predicate, seq):
    for x in seq:
        if not predicate(x): return False
    return True

def some(predicate, seq):
    for x in seq:
        px = predicate(x)
        if px: return px
    return False

def isin(elt, seq):
    for x in seq:
        if elt is x: return True
    return False

def argmin(seq, fn):
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best

def argmin_list(seq, fn):
    best_score, best = fn(seq[0]), []
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = [x], x_score
        elif x_score == best_score:
            best.append(x)
    return best

def argmin_random_tie(seq, fn):
    best_score = fn(seq[0]); n = 0
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score; n = 1
        elif x_score == best_score:
            n += 1
            if random.randrange(n) == 0: best = x
    return best

def argmax(seq, fn): return argmin(seq, lambda x: -fn(x))
def argmax_list(seq, fn): return argmin_list(seq, lambda x: -fn(x))
def argmax_random_tie(seq, fn): return argmin_random_tie(seq, lambda x: -fn(x))

def histogram(values, mode=0, bin_function=None):
    if bin_function: values = map(bin_function, values)
    bins = {}
    for val in values:
        bins[val] = bins.get(val, 0) + 1
    if mode:
        return sorted(bins.items(), key=lambda v: v[1], reverse=True)
    else:
        return sorted(bins.items())

def log2(x): return math.log10(x) / math.log10(2)

def mode(values): return histogram(values, mode=1)[0][0]

def median(values):
    n = len(values)
    values = sorted(values)
    if n % 2 == 1: return values[n // 2]
    else:
        middle2 = values[(n // 2) - 1:(n // 2) + 1]
        try: return mean(middle2)
        except TypeError: return random.choice(middle2)

def mean(values): return sum(values) / float(len(values))

def stddev(values, meanval=None):
    if meanval == None: meanval = mean(values)
    return math.sqrt(sum([(x - meanval) ** 2 for x in values]) / (len(values) - 1))

def dotproduct(X, Y): return sum([x * y for x, y in zip(X, Y)])

def vector_add(a, b): return tuple(map(operator.add, a, b))

def probability(p): return p > random.uniform(0.0, 1.0)

def num_or_str(x):
    if isnumber(x): return x
    try: return int(x)
    except ValueError:
        try: return float(x)
        except ValueError: return str(x).strip()

def normalize(numbers, total=1.0):
    k = total / sum(numbers)
    return [k * n for n in numbers]

orientations = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def turn_right(orientation): return orientations[orientations.index(orientation) - 1]
def turn_left(orientation): return orientations[(orientations.index(orientation) + 1) % len(orientations)]

def distance(t1, t2): return math.hypot((t1[0] - t2[0]), (t1[1] - t2[1]))
def distance2(t1, t2): return (t1[0] - t2[0]) ** 2 + (t1[1] - t2[1]) ** 2

def clip(vector, lowest, highest):
    return type(vector)(map(min, map(max, vector, lowest), highest))

def printf(format, *args):
    sys.stdout.write(str(format) % args)
    return if_(args, args[-1], format)

def caller(n=1):
    import inspect
    return inspect.getouterframes(inspect.currentframe())[n][3]

def memoize(fn, slot=None):
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot): return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        def memoized_fn(*args):
            if args not in memoized_fn.cache:
                memoized_fn.cache[args] = fn(*args)
            return memoized_fn.cache[args]
        memoized_fn.cache = {}
    return memoized_fn

def if_(test, result, alternative):
    if test:
        if callable(result): return result()
        return result
    else:
        if callable(alternative): return alternative()
        return alternative

def name(object):
    return (getattr(object, 'name', 0) or getattr(object, '__name__', 0)
            or getattr(getattr(object, '__class__', 0), '__name__', 0)
            or str(object))

def isnumber(x): return hasattr(x, '__int__')
def issequence(x): return hasattr(x, '__getitem__')

def print_table(table, header=None, sep=' ', numfmt='%g'):
    justs = [if_(isnumber(x), 'rjust', 'ljust') for x in table[0]]
    if header: table = [header] + table
    table = [[if_(isnumber(x), lambda: numfmt % x, x) for x in row] for row in table]
    maxlen = lambda seq: max(map(len, seq))
    sizes = map(maxlen, zip(*[map(str, row) for row in table]))
    for row in table:
        for (j, size, x) in zip(justs, sizes, row):
            print(getattr(str(x), j)(size), sep),
        print()

def AIMAFile(components, mode='r'):
    dir = os.path.dirname(__file__)
    return open(os.path.join(*([dir] + components)), mode)

def DataFile(name, mode='r'):
    return AIMAFile(['..', 'data', name], mode)

class Queue:
    def __init__(self): abstract
    def extend(self, items):
        for item in items: self.append(item)

def Stack(): return []

class FIFOQueue(Queue):
    def __init__(self): self.A = []; self.start = 0
    def append(self, item): self.A.append(item)
    def __len__(self): return len(self.A) - self.start
    def extend(self, items): self.A.extend(items)
    def pop(self):
        e = self.A[self.start]
        self.start += 1
        if self.start > 5 and self.start > len(self.A) / 2:
            self.A = self.A[self.start:]
            self.start = 0
        return e

class PriorityQueue(Queue):
    def __init__(self, order=min, f=lambda x: x):
        update(self, A=[], order=order, f=f)
    def append(self, item):
        bisect.insort(self.A, (self.f(item), item))
    def __len__(self): return len(self.A)
    def pop(self):
        if self.order == min: return self.A.pop(0)[1]
        else: return self.A.pop()[1]

Fig = {}

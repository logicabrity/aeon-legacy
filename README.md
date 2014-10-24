Aeon
====

Measures how often designated functions, methods, or pieces of code are
executed and what their runtime is. Optionally prints a nice report to the
screen, although the raw data is available for further processing as well.

Outline
-------

1. Mark parts of the code that should be monitored with the provided
context manager or decorators.
2. Tell your program to output the report or provide you the data when it's done.
3. Run your program.
4. ?????
5. Profit.

Basic Usage
-----------

How to designate code that should be monitored.

A free-standing piece of code.

```python
from aeon import timer

with timer('my measurement'):
    # do stuff here...

# to assign the measurement to a specific group
with timer('my measurement', 'general frobnication'):
    # do stuff here
```

A function.

```python
from aeon import timer

@timer
def my_function():
    pass
```

A method.

```python
from aeon import timer

class Foo(object):
    @timer.method
    def bar(self):
        pass
```

How to see the report.

```python
from aeon import timer

print timer.report() 
print timer  # equivalent
```

Further features
----------------

You can instantiate your own timer if you want to, in case you want to use
several in parallel.

```python
from aeon import Timer

my_timer= Timer()

with my_timer('my_measurement'):
    pass

# or
with my_timer('my_measurement', 'my_group'):
    pass

@my_timer
def foo():
    pass

class Foo(object):
    @my_timer.method
    def bar(self):
        pass
```

The timer object can be queried for specific measurements or the data
with which it generates the report.

Also, nothing prevents you from using the Measurement class on its own:

```python
from aeon import Measurement

m = Measurement()
for i in xrange(100):
    m.start()
    # stuff happens here
    m.stop()

assert m.calls == 100
print m.total_runtime, m.time_per_call
```

Rationale
---------

The code has originally been used in a computational physics project where
the typical runtime distribution is very dependent on the problem at hand.
It has proven itself useful for giving a feel for where time is spent
during computation and quickly showing when parts of code went on a riot.
In fact, in that project, it is enabled in production since the overhead
is low.

What sets it apart is the possibility to monitor only specific parts of the
code and optionally have these parts logically grouped (by default, it will
use the class or module names).

There are better alternatives for proper benchmarking, like cProfile.

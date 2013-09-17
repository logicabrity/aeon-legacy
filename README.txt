Aeon
====

Measures how often designated functions, methods, or pieces of code are
executed and what their runtime is. Optionally prints a nice report to
the screen, although the raw data is available for further processing as
well.

Outline
-------

1. Mark parts of the code that should be monitored with the provided
   context manager or decorators.
2. Tell your program to output the report or provide you the data when
   it's done.
3. Run your program.
4. ?????
5. Profit.

Basic Usage
-----------

How to designate code that should be monitored.

A free-standing piece of code.

.. code:: python

    from aeon import timed

    with timed('my measurement'):
        # do stuff here...

    # to assign the measurement to a specific group
    with timed('my measurement', 'general frobnication'):
        # do stuff here

A function.

.. code:: python

    from aeon import ftimed

    @ftimed
    def my_function():
        pass

A method.

.. code:: python

    from aeon import mtimed

    class Foo(object):
        @mtimed
        def bar(self):
            pass

How to see the report.

.. code:: python

    from aeon import default_timer

    print default_timer.report() 
    print default_timer  # equivalent

Further features
----------------

The ``timed``, ``ftimed`` and ``mtimed`` helpers all take an optional
``timer`` parameter in case you want to use your own timer or several
timer objects in parallel.

.. code:: python

    from aeon import timed, ftimed, mtimed, Timer

    my_custom_timer = Timer()

    with timed('my_measurement', timer=my_custom_timer):
        pass

    # or
    with timed('my_measurement', 'my_group', my_custom_timer):
        pass

    @ftimed(my_custom_timer)
    def foo():
        pass

    class Foo(object):
        @mtimed(my_custom_timer)
        def bar(self):
            pass

The timer object can be queried for specific measurements or the data
with which it generates the report.

Also, nothing prevents from using the Measurement class on its own:

.. code:: python

    from aeon import Measurement

    m = Measurement()
    for i in xrange(100):
        m.start()
        # stuff happens here
        m.stop()

    assert m.calls == 100
    print m.total_runtime, m.time_per_call

Rationale
---------

The code has originally been used in a computational physics project
where the typical runtime distribution is very dependent on the problem
at hand. It has proven itself useful for giving a feel for where time is
spent during computation and quickly showing when parts of code went on
a riot. In fact, in that project, it is enabled in production since the
overhead is low.

What sets it apart is the possibility to monitor only specific parts of
the code and optionally have these parts logically grouped (by default,
it will use the class or module names).

There are better alternatives for proper benchmarking, like cProfile.

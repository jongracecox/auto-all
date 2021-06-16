"""
Auto-All package

auto_all can be used for controlling what is made available
for import from a package.

There are two main approaches:

    1) Use ``start_all`` and ``end_all`` to wrap all public
       functions and variables.
    2) Use the ``@public`` decorator to identify publicly
       facing functions.

start_all/end_all Approach
==========================

    First, import the auto_all functions.

        >>> from auto_all import start_all, end_all

    If your package has external dependencies then these can be imported
    and the imported objects can be hidden.  In this case we will import
    pathlib.Path and show that it doesn't appear on the __all__ list.

        >>> from pathlib import Path

    Now we can define some internal functions that we want to keep private.
    We can also do this using underscore prefixes, but auto_all gives us a
    little more control.

        >>> def a_private_function():
        ...     print("This is a private function.")

    Now we are ready to start defining public functions, so we use
    ``start_all()``.

        >>> start_all()

    Now we can define our public functions.

        >>> def a_public_function():
        ...     print("This is a public function.")

    Finally we use ``end_all()`` to finish defining public functions and
    create the ``__all__`` variable.

        >>> end_all()

    When we look at the ``__all__`` variable we can see only the public
    facing function is listed.

        >>> print(__all__)
        ['a_public_function']

    It is possible to pass the globals dict to the ``start_all`` and
    ``end_all`` function calls. This is not typically necessary, and is
    only included for backward compatibility.

        >>> del __all__  # Delete __all__ for demo purposes

        >>> start_all(globals())

        >>> def another_public_function():
        ...     pass

        >>> end_all(globals())

        >>> def a_private_function():
        ...     pass

        >>> print(__all__)
        ['another_public_function']

@public decorator approach
==========================

    The second approach is to use the ``@public`` decorator. Note that this
    approach is only suitable for functions, and will not work for declaring
    classes or variables as public.

    First, import the decorator:

        >>> del __all__  # Delete __all__ for demo purposes
        >>> from auto_all import public

    We can define any private functions without any decorator:

        >>> def a_private_function():
        ...     pass

    We can define public functions by decorating with the ``@public``
    decorator:

        >>> @public
        ... def a_public_function():
        ...     pass

    The ``__all__`` variable will only include functions that have been
    declared as public:

        >>> print(__all__)
        ['a_public_function']

Combining the two approaches
============================

    In the event that you need to declare variables and classes as public, and
    also want to make use of the ``@public`` decorator for functions you can
    combine both methods.

        >>> del __all__  # Delete __all__ for demo purposes

    Private variables can be defined outside the start/end block:

        >>> PRIVATE_VARIABLE = "I am private"

    Public items can be defined between the ``start_all()`` and ``end_all()``
    function calls:

        >>> start_all()
        >>> PUBLIC_VARIABLE = "I am public"
        >>> class PublicClass:
        ...     pass
        >>> end_all()

    Private functions can be defined undecorated outside the start/end block:

        >>> def private_function():
        ...     pass

    Public functions can be decorated with the ``@public`` decorator:

        >>> @public
        ... def public_function():
        ...     pass

    The ``__all__`` variable will include any object declared between the
    ``start_all`` and ``end_all`` calls, and any function decorated with the
    ``@public`` decorator:

        >>> print(sorted(__all__))
        ['PUBLIC_VARIABLE', 'PublicClass', 'public_function']

"""
import inspect
from typing import Callable
from typing import Dict, Optional
_GLOBAL_VAR_NAME = '_do_not_include_all'


def _get_globals():
    """Get global dict from stack."""
    calling_module = inspect.stack()[2]
    local_stack = calling_module[0]
    return local_stack.f_globals


def start_all(globs: Optional[Dict] = None):
    """Start defining externally accessible objects.

    Call ``start_all(globals())`` when you want to start defining objects
    in your module that you want to be accessible from outside the module.

    Args:
        globs(dict, optional): Pass the globals dictionary to the function
            using ``globals()``.
    """
    if not globs:
        globs = _get_globals()

    globs[_GLOBAL_VAR_NAME] = list(globs.keys()) + [_GLOBAL_VAR_NAME]


def end_all(globs: Optional[Dict] = None):
    """Finish defining externally accessible objects.

    Call ``end_all(globals())`` when you have finished defining objects
    in your module that you want to be accessible from outside the module.
    After this function has been run the ``__all__`` module variable will
    be updated with the names of all objects that were created between the
    ``start_all`` and ``end_all`` funciton calls.

    Args:
        globs(dict, optional): Pass the globals dictionary to the function
            using ``globals()``.
    """
    if not globs:
        globs = _get_globals()

    globs['__all__'] = list(
        set(list(globs.keys())) - set(globs[_GLOBAL_VAR_NAME])
    )


def public(func: Callable):
    """Decorator that adds a function to the modules __all__ list."""

    local_stack = inspect.stack()[1][0]

    global_vars = local_stack.f_globals

    if '__all__' not in global_vars:
        global_vars['__all__'] = []

    all_var = global_vars['__all__']

    all_var.append(func.__name__)

    return func

__all__ = ['start_all', 'end_all', 'public']

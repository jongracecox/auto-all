# auto-all

Automatically manage the `__all__` variable in Python modules.

[![pypi package](https://badge.fury.io/py/auto-all.svg)](https://pypi.org/project/auto-all)
[![build status](https://api.travis-ci.com/jongracecox/auto-all.svg?branch=master)](https://travis-ci.com/jongracecox/auto-all)
[![downloads](https://img.shields.io/pypi/dm/auto-all.svg)](https://pypistats.org/packages/auto-all)
[![GitHub last commit](https://img.shields.io/github/last-commit/jongracecox/auto-all.svg)](https://github.com/jongracecox/auto-all/commits/master)
[![GitHub](https://img.shields.io/github/license/jongracecox/auto-all.svg)](https://github.com/jongracecox/auto-all/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jongracecox/auto-all.svg?style=social)](https://github.com/jongracecox/auto-all/stargazers)

## Overview

`auto_all` can be used for controlling what is made available
for import from a Python module.

Advantages:

* Easily populate the `__all__` variable in modules.
* Easily exclude imported objects
* Clearly differentiate between internal and external facing objects.
* Use simple, intuitive code.
* Never worry about forgetting to add new objects to `__all__`.
* Help Python IDE's differentiate between internal and external facing objects.

## Installation

```bash
pip install auto-all
```

## Usage

There are two main approaches:

      1) Use `start_all` and `end_all` to wrap all public functions and
         variables.
      2) Use the `@public` decorator to identify publicly facing functions.

### start_all/end_all approach

First, import the auto_all functions into your module.

```python
from auto_all import start_all, end_all
```

If your module has external dependencies then these can be imported
and the imported objects can be hidden.  In this example we will import
pathlib.Path and show that it doesn't appear on the `__all__` list.
We're not actually going to use this import, it's just for illustration.

```python
from pathlib import Path
```

Now we can define some internal functions that we want to keep private.
We can also do this using underscore prefixes, but `auto_all` gives us a
little more granular control.

```python
def a_private_function():
    print("This is a private function.")
```

Now we are ready to start defining public functions, so we use
`start_all()`.

```python
start_all()
```

Now we can define our public functions.

```python
def a_public_function():
    print("This is a public function.")
```

Finally we use `end_all()` to finish defining public functions and
create the `__all__` variable.

```python
end_all()
```

When we look at the `__all__` variable we can see only the public
facing objects are listed.

```
>>> print(__all__)
['a_public_function']
```

Putting this all together, your module should look something like this:

```python
from auto_all import start_all, end_all

from pathlib import Path

def a_private_function():
    print("This is a private function.")

start_all()

def a_public_function():
    print("This is a public function.")

end_all()
```

It is possible to pass the globals dict to the `start_all` and
`end_all` function calls. This is not typically necessary, and is
only included for backward compatibility.

```python
start_all(globals())

def another_public_function():
    pass

end_all(globals())

def a_private_function():
    pass

print(__all__)
```

### `@public` decorator approach

The second approach is to use the `@public` decorator. Note that this
approach is only suitable for functions, and will not work for declaring
classes or variables as public.

First, import the decorator:

```python
from auto_all import public
```

We can define any private functions without any decorator:

```python
def a_private_function():
    pass
```

We can define public functions by decorating with the `@public`
decorator:

```python
@public
def a_public_function():
    pass
```

The `__all__` variable will only include functions that have been
declared as public:

```
>>> print(__all__)
['a_public_function']
```

Combining the two approaches
============================

In the event that you need to declare variables and classes as public, and
also want to make use of the `@public` decorator for functions you can
combine both methods.

Private variables can be defined outside the start/end block:

```python
PRIVATE_VARIABLE = "I am private"
```

Public items can be defined between the `start_all()` and `end_all()`
function calls:

```python
start_all()
PUBLIC_VARIABLE = "I am public"
class PublicClass:
    pass
end_all()
```

Private functions can be defined undecorated outside the start/end block:

```python
def private_function():
pass
```

Public functions can be decorated with the `@public` decorator:

```python
@public
def public_function():
    pass
```

The `__all__` variable will include any object declared between the
`start_all` and `end_all` calls, and any function decorated with the
`@public` decorator:

```
>>> print(__all__)
['PUBLIC_VARIABLE', 'PublicClass', 'public_function']
```

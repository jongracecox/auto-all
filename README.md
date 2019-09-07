# auto-all

Automatically manage the `__all__` variable in Python modules.

[![pypi package](https://badge.fury.io/py/auto-all.svg)](https://pypi.org/project/auto-all)
[![build status](https://api.travis-ci.org/jongracecox/auto-all.svg?branch=master)](https://travis-ci.org/jongracecox/auto-all)
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
`start_all()`.  We need to pass it the globals dict so that it can
see what's already defined.

```python
start_all(globals())
```

Now we can define our public functions.

```python
def a_public_function():
    print("This is a public function.")
```

Finally we use `end_all()` to finish defining public functions and
create the `__all__` variable.

```python
end_all(globals())
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

start_all(globals())

def a_public_function():
    print("This is a public function.")

end_all(globals())
```

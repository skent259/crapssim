# Contributing 

## How to contribute to crapssim

The current top priorities for the package are to improve 
- Documentation
- Supported strategies (see [strategy](https://github.com/sphinx-doc/sphinx/issues/4961)) 
- Reducing bugs and other [issues](https://github.com/skent259/crapssim/issues/)

### Do you want to help the documentation?

There's many ways to improve the documentation for current and future users (including us!):

- Write a short tutorial with some example usage of the package
- Add more descriptions or type hints to internal package functions

### Do you want to help supported strategies?

Craps has so many possible strategies, and it's hard to implement them all. The ultimate goal of the package is to make building strategies easy for end users, but we also want to have commonly used and well known versions available as in the package as examples. 

If you saw a strategy online or in a book, and have implemented with "crapssim", then it most likely makes a great addition to the package. Please mention in [a new discussion](https://github.com/skent259/crapssim/discussions/new), file [an issue](https://github.com/skent259/crapssim/issues/new), or open [a pull request](https://github.com/skent259/crapssim/pulls) and we can work together to make sure it fits well.


### Did you find a bug?

* Please double check the bug has not already been reported in the [Github issues](https://github.com/skent259/crapssim/issues)
* If your issue has not already been reported, [open a new issue](https://github.com/skent259/crapssim/issues/new) with as much detail to reproduce your problem as possible. The more details you provide, the easier it will be to isolate and fix the problem!

## Contributing — Documentation and Examples

### Conventions

* This project uses [the Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) for formatting, which is easily [installed](https://black.readthedocs.io/en/stable/getting_started.html) or available in most IDEs
* Code structure is moving towards [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) unless it conflicts with Black formatting
* Documentation is moving towards [Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) (See also [here](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings))

Please double check these conventions if submitting a PR.

### Function and Type Hinting

All internal functions and classes should include:

- A one-line summary docstring describing purpose and domain.
- Explicit type hints for all parameters and return values.

Example:

```python
def payout_ratio(number: int) -> float:
    """Return the true odds payout ratio for a given point number."""
```

As above, please use [Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) (See also [here](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings))

### Testing Philosophy

Tests are expected to cover both numerical and structural correctness. Each
feature addition should include:

- A unit test verifying direct functional behavior.
- An integration or stress test demonstrating stable interaction with other
  modules.

### Running Tests and Gauntlet

To verify correctness locally:

```bash
pytest -q
```

For optional stress and batch validation:

```bash
pytest -q -m stress
python tools/vxp_gauntlet.py           # single run
bash -lc 'for i in $(seq 1 25); do python tools/vxp_gauntlet.py; sleep 0.2; done'  # batch
```

Artifacts will appear under reports/vxp_gauntlet/<timestamp>/ and include JSON, CSV, and Markdown summaries.

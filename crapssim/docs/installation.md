# Installation

crapssim can be installed in a couple of ways, depending on purpose.

## Official release installation

For a normal user, it is recommended to install the official release. You will
need an installation of python version 3.10 or newer.

```console
pip install crapssim
```

## Development installation

To contribute to the package, you need a few additional steps. With python
version 3.10 or newer, you will need to [fork the repository][fork-repo], clone it
locally, then create a virtual environment and install the package locally in
[editable mode][editable-mode]. Simply copy the following code (replacing your GitHub
username in the first line) into a terminal at the desired directory.

**Linux/Mac**
```console
git clone -b dev https://github.com/<YOUR-GITHUB-USERNAME>/crapssim.git
cd crapssim
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -e .
pip install pytest
```

**Windows**
```console
git clone -b dev https://github.com/<YOUR-GITHUB-USERNAME>/crapssim.git
cd crapssim
python3 -m venv venv
venv\Scripts\activate.bat
python -m pip install -e .
pip install pytest
```

## Latest installation

If you only want to use the latest [development sources][dev-sources] and do not care
about having a cloned repository, e.g. if a bug you care about has been
fixed but an official release has not come out yet, then use this command:

```console
pip install git+https://github.com/skent259/crapssim.git@main
```

[fork-repo]: https://docs.github.com/en/get-started/quickstart/fork-a-repo
[editable-mode]: https://realpython.com/what-is-pip/#installing-packages-in-editable-mode-to-ease-development
[dev-sources]: https://github.com/skent259/crapssim/tree/dev
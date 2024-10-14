# WADAS POC

## Dependencies

See requirements.txt

## Environment setup
Reference Python versions: 3.10 or 3.11.

Reference IDE used for the project is PyCharm, Conda (Miniconda) as package manager.

Instructions will reflect the above-mentioned reference environment, users are free to choose any equivalent environment for development and execution of the project.

### Dependencies install

   1. Import the WADAS project into your IDE
   2. Create venv enviromnent (See https://code.visualstudio.com/docs/python/environments for detailed info about how to create virtual environment within VScode, we used conda.)
   3. Install dependencies:
      a. pip install -r requirements.txt .\poc\requirements.txt (or use miniconda command line/Anaconda navigator UI)

## Run WADAS (with UI)

    1. Run main.py

## Development

We use the [pre-commit framework](https://pre-commit.com/) for hook management. The recommended way of installing it is using pip:

* `pip install pre-commit`

The hooks can then be installed into your local clone using:

* `pre-commit install [--allow-missing-config]`

--allow-missing-config is an optional argument that will allow users to have the hooks installed and be functional even if using an older branch that does not have them tracked. A warning will be displayed for such cases when the hooks are ran.

Uninstalling the hooks can be done using pre-commit uninstall.

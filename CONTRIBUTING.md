# Contributing

All contributions are much welcome and greatly appreciated! Expect to be credited for you effort.

## General

Generally try to limit the scope of any Pull Request to an atomic update if possible. This way, it's much easier to assess and review your changes.

You should expect a considerably faster turn around if you submit two or more PRs instead of baking them all into one major PR.

## Pull Request Guidelines

Good pull requests, patches, improvements, new features are a fantastic
help. They should remain focused in scope and avoid containing unrelated
commits.

**Please ask first** before embarking on any **significant** pull request (e.g.
implementing features, refactoring code, porting to a different language),
otherwise you risk spending a lot of time working on something that the
project's developers might not want to merge into the project. For trivial
things, or things that don't require a lot of your time, you can go ahead and
make a PR.

Please adhere to the [coding guidelines](#Coding-guidelines) used throughout the
project (indentation, accurate comments, etc.) and any other requirements
(such as test coverage).

Adhering to the following process is the best way to get your work included in the project:

1. [Fork](https://help.github.com/articles/fork-a-repo/) the project, clone your fork,
   and configure the remotes:

   ```bash
   # Clone your fork of the repo into the current directory
   git clone https://github.com/<your-username>/applepassgenerator.git
   # Navigate to the newly cloned directory
   cd applepassgenerator
   # Assign the original repo to a remote called "upstream"
   git remote add upstream https://github.com/PrimedigitalGlobal/applepassgenerator.git
   ```

2. If you cloned a while ago, get the latest changes from upstream:

   ```bash
   git checkout main
   git pull upstream main
   ```

3. Setup Python

   Setup base Python with https://www.python.org/downloads/

4. Install Poetry and Setup Project

   - Install [Poetry](https://python-poetry.org/) by following the official installation guide [here](https://python-poetry.org/docs/#installation).
   - All project dependencies are managed using [Poetry](https://python-poetry.org/). The project’s direct dependencies are listed in `pyproject.toml`. Running `poetry lock` generates `poetry.lock` which has all versions pinned.
   - Run `poetry install` to install all project dependencies listed in `poetry.lock`. This ensures that everyone using the library will get the same versions of the dependencies.
   - Run `poetry run pre-commit install` in order to enable all pre-commit hooks.

   Note: The `run` command executes the given command inside the project’s virtualenv create by Poetry.
      - Example: `poetry run python your_script.py`

   Tip: We recommend that you use this workflow and keep `pyproject.toml` as well as `poetry.lock` under version control to make sure all computers and environments run exactly the same code.

5. Create a new topic branch (off the main project development branch) to
   contain your feature, change, or fix:

   ```bash
   git checkout -b <topic-branch-name>
   ```

6. Commit your changes in logical chunks. Please adhere to these [git commit message guidelines](https://www.conventionalcommits.org/en/v1.0.0/) or your code is unlikely be merged into the main project. Use Git's [interactive rebase](https://help.github.com/articles/about-git-rebase/) feature to tidy up your commits before making them public.

7. The pull request should include tests for relevant changes.

8. If the pull request adds functionality, the docs should be updated.

9. Update the changelog present under `docs/changelog.md` following [keep a changelog](https://keepachangelog.com/en/1.0.0/) conventions.

10. Locally merge (or rebase) the upstream development branch into your topic branch:

   ```bash
   git pull [--rebase] upstream main
   ```

11. Push your topic branch up to your fork:

   ```bash
   git push origin <topic-branch-name>
   ```

12. [Open a Pull Request](https://help.github.com/articles/about-pull-requests/)
    with a clear title and description against the `main` branch.

**IMPORTANT**: By submitting a patch, you agree to allow the project owners to
license your work under the terms of the [MIT License](../LICENSE) (if it
includes code changes) and under the terms of the
[Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/)
(if it includes documentation changes).

## Coding guidelines

- Read and pay attention to current code in the repository
- For the Python part, we follow [black](https://pypi.org/project/black/) for formatting code. We use modified configuration of [flake8][flake8] to check for linting errors that complies formatting standards of `black`. Once you're ready to commit changes, format your code with `black` and check your code with `flake8`. Optionally, setup `pre-commit` with `poetry run pre-commit install` to do it automatically before commit.
- Install a plugin for [EditorConfig][editorconfig] and let it handle some formatting issues for you.

[editorconfig]: http://editorconfig.org/
[flake8]: http://flake8.readthedocs.org/en/latest/

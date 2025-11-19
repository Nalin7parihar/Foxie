# Publishing Foxie CLI to PyPI

This guide explains how to publish the `foxie-cli` package to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org/account/register/
2. **TestPyPI Account** (optional, for testing): Create an account at https://test.pypi.org/account/register/
3. **Build Tools**: Install build tools:
   ```bash
   pip install build twine
   ```

## Publishing Steps

### 1. Update Version

Before publishing, update the version in `pyproject.toml`:

```toml
[project]
version = "0.1.0"  # Update this (e.g., "0.1.1", "0.2.0", etc.)
```

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

### 2. Build the Package

From the `foxie-cli` directory:

```bash
cd foxie-cli
python -m build
```

This creates:

- `dist/foxie-cli-<version>.tar.gz` (source distribution)
- `dist/foxie_cli-<version>-py3-none-any.whl` (wheel distribution)

### 3. Test on TestPyPI (Recommended)

First, test your package on TestPyPI:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ foxie-cli
```

### 4. Publish to PyPI

Once tested, publish to the real PyPI:

```bash
python -m twine upload dist/*
```

You'll be prompted for your PyPI username and password. For better security, use an API token:

1. Go to https://pypi.org/manage/account/token/
2. Create a new API token
3. Use `__token__` as username and the token as password

### 5. Verify Installation

After publishing, verify the package can be installed:

```bash
pip install foxie-cli
foxie --help
```

## Automated Publishing with GitHub Actions

You can set up automated publishing using GitHub Actions. Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install build tools
        run: pip install build twine

      - name: Build package
        working-directory: ./foxie-cli
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        working-directory: ./foxie-cli
        run: python -m twine upload dist/*
```

Then:

1. Add `PYPI_API_TOKEN` to your GitHub repository secrets
2. Create a new release on GitHub to trigger the workflow

## Notes

- The package name on PyPI is `foxie-cli` (with hyphen)
- The Python package name is `foxie_cli` (with underscore)
- Make sure to update the version number before each release
- Test thoroughly before publishing to production PyPI
- The backend URL defaults to `http://127.0.0.1:8000` but can be overridden with `FOXIE_BACKEND_URL` environment variable

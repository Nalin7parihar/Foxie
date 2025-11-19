# Publishing Foxie CLI to PyPI

This guide explains how to publish the `foxie-cli` package to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org/account/register/
2. **TestPyPI Account** (optional, for testing): Create an account at https://test.pypi.org/account/register/
3. **Build Tools**: Install build tools:
   ```bash
   pip install build twine
   ```

## Quick Publishing Steps

### Step 1: Navigate to CLI Directory

```bash
cd foxie-cli
```

### Step 2: Clean Previous Builds (Optional)

Remove any old build artifacts:

**Windows PowerShell:**

```powershell
Remove-Item -Recurse -Force dist, build, *.egg-info, src\*.egg-info -ErrorAction SilentlyContinue
```

**Linux/macOS:**

```bash
rm -rf dist/ build/ *.egg-info/ src/*.egg-info/
```

### Step 3: Update Version (if needed)

Edit `pyproject.toml` and update the version:

```toml
[project]
version = "0.1.0"  # Update this (e.g., "0.1.1", "0.2.0", etc.)
```

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

### Step 4: Build the Package

```bash
python -m build
```

This creates:

- `dist/foxie-cli-<version>.tar.gz` (source distribution)
- `dist/foxie_cli-<version>-py3-none-any.whl` (wheel distribution)

### Step 5: Get PyPI API Token

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Give it a name (e.g., "foxie-cli-publish")
4. Set scope to "Entire account" (or just this project)
5. **Copy the token** (you'll only see it once! It starts with `pypi-`)

### Step 6: Upload to PyPI

```bash
python -m twine upload dist/*
```

When prompted:

- **Username:** `__token__` (with underscores, exactly as shown)
- **Password:** Your PyPI API token (paste the token you copied)

### Step 7: Verify Installation

After publishing, verify the package can be installed:

```bash
pip install foxie-cli
foxie --help
```

If you see the help message, you're done! 🎉

## Testing on TestPyPI (Recommended)

Before publishing to production PyPI, test on TestPyPI:

### TestPyPI Setup

1. Create a TestPyPI account: https://test.pypi.org/account/register/
2. Get a TestPyPI API token: https://test.pypi.org/manage/account/token/

### Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

When prompted:

- **Username:** `__token__`
- **Password:** Your TestPyPI API token

### Test Installation from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ foxie-cli
foxie --help
```

If it works, proceed to publish to the real PyPI!

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

## Troubleshooting

### "Package already exists" Error

- Update the version in `pyproject.toml` and rebuild
- You cannot overwrite an existing version on PyPI

### "Invalid credentials" Error

- Make sure you're using `__token__` as username (with underscores, exactly as shown)
- Verify your API token is correct (copy-paste carefully, no extra spaces)
- Make sure you're using the correct token (PyPI vs TestPyPI)

### "File already exists" Error

- Delete old files from `dist/` directory
- Or update the version number

### Build Errors

- Make sure you're in the `foxie-cli` directory
- Ensure `pyproject.toml` is valid
- Check that all dependencies are listed correctly

## Important Notes

- **Package name on PyPI:** `foxie-cli` (with hyphen)
- **Python package name:** `foxie_cli` (with underscore)
- **Command after installation:** `foxie`
- **Backend URL:** Defaults to `https://foxie-wsj6.onrender.com` but can be overridden with `FOXIE_BACKEND_URL` environment variable (useful for local development)
- **Version updates:** Always update the version number in `pyproject.toml` before each release
- **Testing:** Test thoroughly before publishing to production PyPI

## Quick Reference

```bash
# Full workflow (after prerequisites):
cd foxie-cli
python -m build
python -m twine upload dist/*
```

## Next Steps After Publishing

1. ✅ Test installation on a clean environment
2. ✅ Update documentation with installation instructions
3. ✅ Share your package! 🚀
4. ✅ Monitor PyPI for downloads and issues

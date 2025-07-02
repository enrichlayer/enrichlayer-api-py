# Publishing enrichlayer-api to PyPI

This guide covers the steps to publish the `enrichlayer-api` package to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (for testing)

2. **API Tokens**: Generate API tokens for both PyPI and TestPyPI:
   - Go to Account Settings → API tokens
   - Create a token with "Entire account" scope

3. **Poetry**: Ensure Poetry is installed:
   ```bash
   pip install poetry
   ```

## Pre-Publishing Checklist

1. **Update Version**: In `pyproject.toml`, update the version number:
   ```toml
   version = "0.1.0"  # Remove .post2 for clean release
   ```

2. **Verify Metadata**: Ensure all metadata in `pyproject.toml` is correct:
   - description
   - authors
   - license
   - homepage
   - repository
   - documentation
   - keywords
   - classifiers

3. **Run Tests**:
   ```bash
   # Run all tests
   python -m pytest tests/
   
   # Run linting
   ruff check .
   
   # Run type checking
   mypy enrichlayer_client/
   ```

4. **Build Package**:
   ```bash
   poetry build
   ```
   This creates files in `dist/`:
   - `enrichlayer_api-0.1.0-py3-none-any.whl`
   - `enrichlayer_api-0.1.0.tar.gz`

## Publishing to TestPyPI (Recommended First)

1. **Configure Poetry for TestPyPI**:
   ```bash
   poetry config repositories.test-pypi https://test.pypi.org/legacy/
   poetry config pypi-token.test-pypi <your-test-pypi-token>
   ```

2. **Publish to TestPyPI**:
   ```bash
   poetry publish -r test-pypi
   ```

3. **Test Installation from TestPyPI**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ enrichlayer-api[gevent]
   ```

4. **Verify the package works**:
   ```python
   from enrichlayer_client.gevent import EnrichLayer
   client = EnrichLayer(api_key="your-test-key")
   print("Package installed successfully!")
   ```

## Publishing to PyPI (Production)

1. **Configure Poetry for PyPI**:
   ```bash
   poetry config pypi-token.pypi <your-pypi-token>
   ```

2. **Publish to PyPI**:
   ```bash
   poetry publish
   ```

3. **Verify on PyPI**:
   - Visit https://pypi.org/project/enrichlayer-api/
   - Check that all metadata displays correctly

4. **Test Installation**:
   ```bash
   pip install enrichlayer-api[gevent]
   # or
   pip install enrichlayer-api[asyncio]
   # or
   pip install enrichlayer-api[twisted]
   ```

## Post-Publishing Steps

1. **Create Git Tag**:
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

2. **Create GitLab Release**:
   - Go to GitLab repository → Deployments → Releases → New Release
   - Select the tag you created
   - Add release notes

3. **Update Documentation**:
   - Update any documentation with the new version
   - Update installation instructions if needed

4. **Announce the Release**:
   - Blog post
   - Social media
   - Email newsletter

## Version Management

For subsequent releases:
1. Update version in `pyproject.toml`
2. Update CHANGELOG.md (if you have one)
3. Commit changes
4. Build and publish
5. Tag the release

## Troubleshooting

1. **Package name already taken**: The name `enrichlayer-api` should be available, but if not, consider:
   - `enrichlayer`
   - `enrichlayer-client`
   - `enrichlayer-python`

2. **Build errors**: Ensure all dependencies are specified correctly in `pyproject.toml`

3. **Authentication errors**: Regenerate API tokens and ensure they're correctly configured

4. **Missing files in package**: Check that all necessary files are included via `packages` in `pyproject.toml`

## Security Notes

- Never commit API tokens to git
- Use environment variables or Poetry config for tokens
- Consider using GitLab CI/CD for automated publishing (with secrets)

## Automated Publishing with GitLab CI/CD (Optional)

Create `.gitlab-ci.yml`:
```yaml
stages:
  - test
  - build
  - publish

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

test:
  stage: test
  image: python:3.9
  script:
    - pip install poetry
    - poetry install
    - poetry run pytest tests/
    - poetry run ruff check .
    - poetry run mypy enrichlayer_client/
  only:
    - branches
    - merge_requests

build:
  stage: build
  image: python:3.9
  script:
    - pip install poetry
    - poetry build
  artifacts:
    paths:
      - dist/
  only:
    - tags

publish-to-pypi:
  stage: publish
  image: python:3.9
  script:
    - pip install poetry
    - poetry config pypi-token.pypi $PYPI_TOKEN
    - poetry publish
  dependencies:
    - build
  only:
    - tags
  when: manual  # Requires manual approval

publish-to-test-pypi:
  stage: publish
  image: python:3.9
  script:
    - pip install poetry
    - poetry config repositories.test-pypi https://test.pypi.org/legacy/
    - poetry config pypi-token.test-pypi $TEST_PYPI_TOKEN
    - poetry publish -r test-pypi
  dependencies:
    - build
  only:
    - tags
  when: manual  # Requires manual approval
```

Remember to add `PYPI_TOKEN` and `TEST_PYPI_TOKEN` to your GitLab project's CI/CD variables (Settings → CI/CD → Variables).
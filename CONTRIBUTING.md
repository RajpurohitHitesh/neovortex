# Contributing to NeoVortex

Thank you for your interest in contributing to **NeoVortex**, a modern, high-performance HTTP client library for Python 3.9+! We welcome contributions from developers of all skill levels, whether you're fixing bugs, adding new features, improving documentation, or creating plugins. This guide provides a detailed, step-by-step process to help you contribute effectively, ensuring a smooth experience for both new and experienced coders.

## Table of Contents
1. [Why Contribute?](#why-contribute)
2. [Getting Started](#getting-started)
   - [Fork the Repository](#fork-the-repository)
   - [Clone and Set Up](#clone-and-set-up)
   - [Install Dependencies](#install-dependencies)
3. [Contribution Workflow](#contribution-workflow)
   - [Find an Issue](#find-an-issue)
   - [Create a Branch](#create-a-branch)
   - [Make Changes](#make-changes)
   - [Write Tests](#write-tests)
   - [Run Tests and Linting](#run-tests-and-linting)
   - [Commit Changes](#commit-changes)
   - [Push and Create a Pull Request](#push-and-create-a-pull-request)
4. [Coding Guidelines](#coding-guidelines)
   - [Code Style](#code-style)
   - [Type Hints](#type-hints)
   - [Documentation](#documentation)
   - [Testing](#testing)
5. [Contributing New Plugins](#contributing-new-plugins)
   - [Plugin Structure](#plugin-structure)
   - [Example Plugin](#example-plugin)
   - [Registering Plugins](#registering-plugins)
   - [Testing Plugins](#testing-plugins)
6. [Common Contribution Types](#common-contribution-types)
   - [Bug Fixes](#bug-fixes)
   - [Feature Additions](#feature-additions)
   - [Documentation Improvements](#documentation-improvements)
   - [Performance Enhancements](#performance-enhancements)
7. [Code Review Process](#code-review-process)
8. [Community Guidelines](#community-guidelines)
9. [Contact and Support](#contact-and-support)
10. [Current Contributors](#current-contributors)

## Why Contribute?
Contributing to NeoVortex allows you to:
- Enhance a widely-used HTTP client library for Python.
- Gain experience in open-source development.
- Improve your Python skills, including asyncio, HTTP protocols, and plugin systems.
- Help developers worldwide by adding features or fixing bugs.
- Be recognized as a contributor to a project led by Hitesh Rajpurohit.

Whether you're a beginner fixing a typo or an expert adding a new plugin, every contribution counts!

## Getting Started
Follow these steps to set up your development environment and start contributing.

### Fork the Repository
1. Go to the NeoVortex repository: [rajpurohithitesh/neovortex](https://github.com/rajpurohithitesh/neovortex).
2. Click the **Fork** button in the top-right corner to create a copy under your GitHub account.
3. This creates a repository at `https://github.com/your-username/neovortex`.

### Clone and Set Up
Clone your forked repository to your local machine:
```bash
git clone https://github.com/your-username/neovortex.git
cd neovortex
```

Add the upstream repository to sync with the main project:
```bash
git remote add upstream https://github.com/rajpurohithitesh/neovortex.git
```

### Install Dependencies
NeoVortex requires Python 3.9 or higher. Install the dependencies listed in `requirements.txt`:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `httpx[http2]>=0.23.0`
- `aiohttp>=3.8.0`
- `pydantic>=1.10.0`
- `oauthlib>=3.2.0`
- `requests-oauthlib>=1.3.0`
- `pyjwt>=2.6.0`
- `redis>=4.5.0`
- `prometheus-client>=0.16.0`
- `websockets>=10.4`
- `click>=8.1.0`
- `pytest>=7.2.0`
- `cryptography>=42.0.0`
- `boto3>=1.28.0`
- `botocore>=1.31.0`
- `sentry-sdk>=1.30.0`
- `elasticsearch>=8.0.0`
- `jsonschema>=4.17.0`
- `xmltodict>=0.13.0`
- `graphql-core>=3.2.0`
- `PyYAML>=6.0.0`
- `hvac>=1.0.0`

Additionally, install development tools:
```bash
pip install flake8 pytest-asyncio
```

## Contribution Workflow
Follow this workflow to contribute changes to NeoVortex.

### Find an Issue
1. Check the [Issues](https://github.com/rajpurohithitesh/neovortex/issues) page for open tasks.
2. Look for issues labeled **good first issue** if you're new to the project.
3. Comment on the issue to express interest (e.g., "I'd like to work on this!").
4. If no suitable issue exists, create a new one to propose a feature or report a bug.

### Create a Branch
Create a branch for your changes with a descriptive name:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number-description
```

Examples:
- `feature/add-oauth-cache-plugin`
- `bugfix/123-fix-rate-limiter`

### Make Changes
Make your changes in the appropriate files:
- Core functionality: `neovortex/` (e.g., `client.py`, `async_client.py`).
- Plugins: `neovortex/plugins/` or `neovortex/plugins/custom/`.
- Tests: `tests/`.
- Documentation: `README.md`, `README-Plugins.md`, or `CONTRIBUTING.md`.

### Write Tests
Add tests to ensure your changes work correctly. Place tests in the `tests/` directory, following the existing structure:
- Unit tests for core features: `tests/test_client.py`, `tests/test_async_client.py`.
- Plugin tests: `tests/test_plugins.py`.
- Utility tests: `tests/test_utils.py`.

**Example Test**:
```python
import pytest
from neovortex.request import NeoVortexRequest
from neovortex.plugins.custom.custom_header import CustomHeaderPlugin

def test_custom_header_plugin():
    plugin = CustomHeaderPlugin(header_name="X-Test", header_value="TestValue")
    request = NeoVortexRequest("GET", "https://example.com")
    processed = plugin.process_request(request)
    assert processed.headers["X-Test"] == "TestValue"
```

### Run Tests and Linting
Before committing, verify your changes:
1. Run tests:
   ```bash
   pytest tests/ --verbose
   ```
   Ensure all tests pass, including async tests (handled by `pytest-asyncio`).

2. Run linting with flake8:
   ```bash
   flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
   flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
   ```
   Fix any errors or warnings reported by flake8.

### Commit Changes
Write clear, concise commit messages following the format:
```
<short description>
<blank line>
<optional detailed description>
```

Example:
```
Add custom header plugin
Adds a new plugin to add custom headers to requests with configurable name and value.
Includes tests and updates README-Plugins.md.
```

Commit your changes:
```bash
git add .
git commit -m "Add custom header plugin"
```

### Push and Create a Pull Request
Push your branch to your fork:
```bash
git push origin feature/your-feature-name
```

Create a pull request (PR):
1. Go to your fork on GitHub (`https://github.com/your-username/neovortex`).
2. Click **Compare & pull request**.
3. Set the base branch to `main` and the compare branch to your feature branch.
4. Write a detailed PR description, including:
   - What the PR does.
   - Related issue number (e.g., "Fixes #123").
   - Any testing or setup instructions.
5. Submit the PR.

## Coding Guidelines
To maintain consistency and quality, follow these guidelines.

### Code Style
- Adhere to **PEP 8** for Python code style.
- Use **flake8** to enforce style rules:
  - Max line length: 127 characters.
  - Max complexity: 10 (Cyclomatic complexity).
  - Check for syntax errors and undefined names (`E9,F63,F7,F82`).
- Use 4 spaces for indentation (no tabs).
- Name variables and functions descriptively (e.g., `process_request` instead of `proc_req`).

**Example**:
```python
def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
    request.headers["X-Example"] = "Value"
    return request
```

### Type Hints
- Use type hints for all functions and methods to support `mypy`.
- Import types from `typing` (e.g., `Optional`, `Dict`).
- Use `NeoVortexRequest` and `NeoVortexResponse` for plugin methods.

**Example**:
```python
from typing import Optional
from neovortex.request import NeoVortexRequest

def add_header(request: NeoVortexRequest, header: Optional[str] = None) -> NeoVortexRequest:
    if header:
        request.headers["X-Custom"] = header
    return request
```

### Documentation
- Update documentation for new features or plugins in `README.md` or `README-Plugins.md`.
- Write clear docstrings for classes, methods, and functions using Google style.
- Include examples in docstrings where applicable.

**Example**:
```python
class CustomPlugin:
    """Adds a custom header to requests.

    Args:
        header_name (str): Name of the header to add.
        header_value (str): Value of the header.

    Example:
        plugin = CustomPlugin("X-Test", "Value")
        request = plugin.process_request(NeoVortexRequest("GET", "https://example.com"))
    """
```

### Testing
- Write tests for all new code using `pytest`.
- Cover both happy paths and edge cases.
- Use `pytest-asyncio` for async tests.
- Place tests in the appropriate `tests/` file (e.g., `test_plugins.py` for plugins).
- Ensure 100% test coverage for new features (use `pytest-cov` if needed).

**Example**:
```python
@pytest.mark.asyncio
async def test_async_request():
    async with AsyncNeoVortexClient() as client:
        response = await client.request("GET", "https://httpbin.org/get")
        assert response.status_code == 200
```

## Contributing New Plugins
Plugins are a core part of NeoVortex's extensibility. Here's how to create and contribute a new plugin.

### Plugin Structure
A plugin is a Python class in `neovortex/plugins/custom/` with optional methods:
- `process_request(request: NeoVortexRequest) -> NeoVortexRequest`: Modifies the request.
- `process_response(request: NeoVortexRequest, response: NeoVortexResponse) -> NeoVortexResponse`: Modifies the response.
- Other methods (e.g., `track_request`, `cache_response`) for specific functionality.

### Example Plugin
**File**: `neovortex/plugins/custom/custom_header.py`
```python
from neovortex.request import NeoVortexRequest
from neovortex.response import NeoVortexResponse

class CustomHeaderPlugin:
    """Adds a custom header to requests and logs response size.

    Args:
        header_name (str): Name of the header to add.
        header_value (str): Value of the header.
    """
    def __init__(self, header_name: str, header_value: str):
        self.header_name = header_name
        self.header_value = header_value

    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        request.headers[self.header_name] = self.header_value
        return request

    def process_response(self, request: NeoVortexRequest, response: NeoVortexResponse) -> NeoVortexResponse:
        print(f"Response size: {len(response.content)} bytes")
        return response
```

### Registering Plugins
1. **Update `neovortex/plugins/__init__.py`**:
   ```python
   from .custom.custom_header import CustomHeaderPlugin

   __all__ = [
       # Existing plugins
       "CustomHeaderPlugin",
       "registry",
   ]
   ```

2. **Add to `PluginRegistry._initialize_plugins`** (if no parameters required):
   ```python
   def _initialize_plugins(self):
       if not self._initialized:
           # Existing registrations
           self.register("custom_header", CustomHeaderPlugin("X-Custom", "DefaultValue"))
           self._initialized = True
   ```

3. **Manual Registration** (if parameters required):
   - Document that the plugin must be registered manually:
     ```python
     custom_header = CustomHeaderPlugin("X-Custom", "MyValue")
     client.register_plugin("custom_header", custom_header)
     client.enable_plugin("custom_header")
     ```

### Testing Plugins
Create a test in `tests/test_plugins.py`:
```python
import pytest
from neovortex.request import NeoVortexRequest
from neovortex.plugins.custom.custom_header import CustomHeaderPlugin

def test_custom_header_plugin():
    plugin = CustomHeaderPlugin(header_name="X-Test", header_value="TestValue")
    request = NeoVortexRequest("GET", "https://example.com")
    processed = plugin.process_request(request)
    assert processed.headers["X-Test"] == "TestValue"
```

Update `README-Plugins.md` with the plugin's details, including configuration, use cases, and examples.

## Common Contribution Types
Here are common ways to contribute to NeoVortex.

### Bug Fixes
- Identify a bug via an issue or testing.
- Reproduce the bug with a minimal test case.
- Fix the bug and add a test to prevent regression.
- Example: Fix a rate limiter bug by adjusting the token bucket algorithm.

### Feature Additions
- Propose a new feature via an issue (e.g., a new plugin or authentication method).
- Implement the feature with tests and documentation.
- Example: Add a plugin for OAuth token caching.

### Documentation Improvements
- Improve clarity in `README.md`, `README-Plugins.md`, or `CONTRIBUTING.md`.
- Add examples or fix typos.
- Example: Expand the plugin guide with more examples.

### Performance Enhancements
- Optimize code for speed or memory usage.
- Profile performance with tools like `cProfile`.
- Example: Improve connection pooling in `client.py`.

## Code Review Process
1. **Submit PR**: Your PR will be reviewed by maintainers (e.g., Hitesh Rajpurohit).
2. **Feedback**: Expect comments on code style, tests, or functionality within 1-3 days.
3. **Revisions**: Address feedback by pushing additional commits to your branch.
4. **Approval**: Once approved, the PR will be merged into `main`.
5. **CI Checks**: Ensure all CI workflows (`ci.yml`, `python-package.yml`, etc.) pass before merging.

**Tips for a Smooth Review**:
- Keep PRs small and focused.
- Reference the issue number in the PR description.
- Respond promptly to feedback.

## Community Guidelines
- Be respectful and inclusive in all interactions.
- Provide constructive feedback in issues and PRs.
- Follow the [Code of Conduct](https://github.com/rajpurohithitesh/neovortex/blob/main/CODE_OF_CONDUCT.md) (if available).
- Ask questions if you're unsure—there's no such thing as a silly question!

## Contact and Support
- **Issues**: Report bugs or propose features on the [Issues](https://github.com/rajpurohithitesh/neovortex/issues) page.
- **Discussions**: Join discussions on the [Discussions](https://github.com/rajpurohithitesh/neovortex/discussions) page (if enabled).
- **GitHub**: Reach out to [rajpurohithitesh](https://github.com/rajpurohithitesh).

If you're new to open source, feel free to ask for guidance in an issue or discussion. We're here to help!

## Current Contributors
- **Hitesh Rajpurohit** ([rajpurohithitesh](https://github.com/rajpurohithitesh)): Creator and lead maintainer.
  - Designed the core architecture, plugin system, and initial features.
  - Maintains the repository and reviews contributions.

Your name could be here! Contribute to NeoVortex and become part of our growing community.

---

Thank you for contributing to NeoVortex! Your efforts help make this library a powerful tool for Python developers worldwide. Let's build something amazing together!
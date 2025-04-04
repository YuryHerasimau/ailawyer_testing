# AI Lawyer Testing Framework

## Overview

End-to-end test automation framework for AI Lawyer web application using Playwright and Pytest. Implements Page Object Model (POM) pattern for maintainable and scalable test architecture.

## Key Features

- 🚀 **Cross-browser testing** support (Chromium, Firefox, WebKit)
- 📄 **Page Object Model** for clean separation of concerns
- 🔐 **Secure credential handling** via environment variables
- 📊 **Parallel test execution** capability
- 🎥 **Auto-waiting and tracing** built-in
- 🔍 **Powerful locators** with text, CSS and XPath support

## Project structure

```
ailawyer_testing/
├── pages/                     # Page Object classes
│   ├── login_page.py
│   ├── google_auth_page.py
│   └── chat_page.py
├── tests/                     # Test cases
│   ├── test_login.py
│   ├── test_chat.py
│   ├── test_chat_settings.py
│   ├── test_prompts.py
│   └── ...
├── .env
├── .gitignore
├── conftest.py
├── pytest.ini
└── requirements.txt
```

# Technology Stack

| Component       | Technology |
|----------------|------------|
| Test Runner    | Pytest |
| Browser Automation | Playwright |
| Language       | Python 3.10+ |
| Reporting      | Built-in Playwright traces |
| CI/CD Ready    | GitHub Actions compatible |

# Getting Started

### Prerequisites

- Python 3.10+
- Git

## Installation

1. Clone repository:
``` bash
git clone https://github.com/YuryHerasimau/ailawyer_testing.git
cd ailawyer_testing
```

2. Set up virtual environment::
``` bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

3. Install dependencies:
``` bash
pip install -r requirements.txt
playwright install
```

## Configuration

1. Create `.env` file:
```ini
GOOGLE_EMAIL=your@email.com
GOOGLE_PASS=yourpassword
```

2. Configure test options in `pytest.ini`:
```ini
[pytest]
addopts = -v --headed
markers =
    smoke: most critical tests
    regression: full feature tests
    flaky: mark flaky tests to rerun
```

## Running Tests

Run all tests:
``` bash

```

Run specific test file:
``` bash
pytest tests/test_prompts.py
```

| Command       | Description |
|----------------|------------|
| `pytest`    | Run all tests |
| `pytest tests/test_prompts.py` | Run specific test suite |
| `pytest -k test_select_prompt` | Run specific test case |
| `pytest -m smoke`       | Run smoke tests only |

## Debugging Tests

1. Run with debug mode:
```bash
PWDEBUG=1 pytest tests/test_login.py
```
or
```bash
PWDEBUG=console pytest -k 'test_initial_ai_greeting'
```

2. Record new test:
```bash
playwright codegen --ignore-https-errors https://app.ailawyer.pro
```

# Contributing

1.  Create feature branch:
```bash
git checkout -b feature/new-test-module
```

2. Add tests following POM pattern
3. Verify tests pass:
```bash
pytest && flake8
```

4. Submit pull request with:

* Description of changes
* Screenshots if UI changes
* Updated documentation
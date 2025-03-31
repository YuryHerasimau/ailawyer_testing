# AI Lawyer Testing Framework

## Overview

AI Lawyer Testing Framework is a testing framework designed to automate UI testing for the legal AI assistant.

## About Playwright

Playwright works with three different layers that build on each other: `Browser`, `Context` and `Page`.

* **Browsers**

    Each version of Playwright requires specific browser versions to run. Unlike Selenium, Playwright does not use webdriver. With each new release, Playwright updates the browser versions it supports. This means that every time you update Playwright, you may have to re-run the ```playwright install``` command

    For `Google Chrome`, `Microsoft Edge` and `other Chromium-based browsers`, Playwright uses open-source Chromium builds by default.

* **BrowserContext**

    Playwright uses browser contexts to achieve test isolation. Pages in two separate contexts do not share cookies, profile settings. A context is an independent browser session, similar to incognito mode. Unlike `Selenium`, they do not require their own browser process. A test can simply open a new context to get a clean environment. Typically, each test has its own context.

* **Pages**

    A Page contains the content of the loaded website. Each Context can have multiple pages. It is used to navigate URLs and interact with the page content.

## Project structure

```
ailawyer_testing/
├── pages/                     # Page objects
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

# Technologies Used

* `Python 3.x` – Main programming language
* `pytest` – Testing framework
* `requests`
* `playwright`
* `pytest-playwright`

# Getting Started

## Installation

Clone the repository:
``` bash
git clone https://github.com/YuryHerasimau/ailawyer_testing.git
cd ailawyer_testing
```

Create and activate a virtual environment:
``` bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

Install dependencies:
``` bash
pip install -r requirements.txt
```

After installing `playwright`, install the necessary browsers:
```bash
playwright install
```

Playwright downloads Chromium, WebKit, and Firefox browsers to OS cache folders:

* %USERPROFILE%\AppData\Local\ms-playwright # on Windows
* ~/Library/Caches/ms-playwright # on MacOS
* ~/.cache/ms-playwright # on Linux

Playwright downloads three browsers by default: Chromium, Firefox, and WebKit.

To install a specific browser, pass it as an argument during installation

```bash
playwright install firefox
```

Recording a Script with Codegen
```bash
playwright codegen --ignore-https-errors https://app.ailawyer.pro
```

## Running Tests

Run all tests:
``` bash
pytest
```

Run specific test file:
``` bash
pytest tests/test_prompts.py
```

## Debug

Debug tools
```bash
PWDEBUG=1 pytest -k 'test_initial_ai_greeting'
```

```bash
PWDEBUG=console pytest -k 'test_initial_ai_greeting'
```

## Configuration

Configure test behavior in `pytest.ini`:

```ini
[pytest]
addopts = -v --headed
testpaths = tests
python_files = test_*.py
python_functions = test_*
```

# Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

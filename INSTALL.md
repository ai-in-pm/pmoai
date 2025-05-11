# Installing PMOAI

This document provides instructions for installing PMOAI (Project Management Office AI Agents).

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- An OpenAI API key (or other supported LLM provider)

## Installation Options

### Option 1: Install from PyPI (Recommended)

```bash
pip install pmoai
```

### Option 2: Install from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/pmoai/pmoai.git
   cd pmoai
   ```

2. Run the installation script:
   ```bash
   python install.py
   ```

   This will install PMOAI in development mode, allowing you to make changes to the code.

### Option 3: Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pmoai/pmoai.git
   cd pmoai
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Verifying the Installation

To verify that PMOAI is installed correctly, run:

```bash
python examples/verify_installation.py
```

You should see output confirming the PMOAI version and available components.

## Configuration

PMOAI requires an API key for the language model provider. You can set this as an environment variable:

```bash
# For OpenAI models (default)
export OPENAI_API_KEY=your-api-key  # Linux/Mac
set OPENAI_API_KEY=your-api-key     # Windows
```

Alternatively, you can create a `.env` file in your project directory with these variables. See `.env.example` for a template.

## Running Tests

To run the tests, execute:

```bash
python run_tests.py
```

## Troubleshooting

If you encounter any issues during installation:

1. Make sure you have Python 3.9 or higher installed:
   ```bash
   python --version
   ```

2. Ensure pip is up to date:
   ```bash
   pip install --upgrade pip
   ```

3. Check that you have set your API key correctly.

4. If you're installing from source, make sure you're in the correct directory.

5. If you're still having issues, please open an issue on the [GitHub repository](https://github.com/pmoai/pmoai/issues).

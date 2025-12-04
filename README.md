# archive-MeTTa

## Python Environment Setup

Before installing dependencies, set up a Python virtual environment to isolate project dependencies.

### 1. Create a Virtual Environment

Navigate to the project directory and create a virtual environment:

```bash
cd /path/to/archive-MeTTa
python3 -m venv .venv
```

Alternatively, you can use `virtualenv`:

```bash
python3 -m pip install --user virtualenv
virtualenv .venv
```

### 2. Activate the Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

After activation, your terminal prompt should show `(.venv)` indicating the virtual environment is active.

### 3. Upgrade pip

Ensure you have the latest version of pip:

```bash
pip install --upgrade pip
```

### 4. Configure PYTHONPATH for Hyperon

After installing hyperon (see installation instructions below), you'll need to add the hyperon path to your environment. This is automatically added to the activation script, but you can verify it's set:

```bash
# The activation script should include this line:
export PYTHONPATH="/path/to/hyperon-experimental/python:$PYTHONPATH"
```

If it's not automatically set, add it manually to `.venv/bin/activate`:

```bash
echo 'export PYTHONPATH="/path/to/hyperon-experimental/python:$PYTHONPATH"' >> .venv/bin/activate
```

**Note:** Replace `/path/to/hyperon-experimental` with the actual path where you cloned the hyperon-experimental repository.

### 5. Deactivating the Virtual Environment

When you're done working, you can deactivate the virtual environment:

```bash
deactivate
```

## Installation

This project requires two main dependencies: `supabase` and `hyperon`.

### Prerequisites

- Python 3.8 or later
- pip (23.1.2 or later)
- Rust (latest stable version) - [Install Rust](https://www.rust-lang.org/tools/install)
- CMake (3.24 or later)
- GCC (7.5 or later) or equivalent C/C++ compiler
- Conan (C++ package manager)

### Installing Supabase

Supabase can be installed directly from PyPI:

```bash
pip install supabase
```

### Installing Hyperon

Hyperon is not available on PyPI and must be installed from source. Follow these steps:

#### 1. Clone the hyperon-experimental repository

```bash
cd /path/to/your/projects
git clone https://github.com/mvpeterson/hyperon-experimental.git
cd hyperon-experimental
```

#### 2. Install build prerequisites

Install `cbindgen` (Rust tool for generating C bindings):

```bash
cargo install --force cbindgen
```

Install `conan` (C++ package manager):

```bash
pip install conan==2.19.1
conan profile detect --force
```

**Note for macOS users:** If you encounter compiler version errors, you may need to update your Conan profile. Edit `~/.conan2/profiles/default` and ensure:
- `compiler=apple-clang`
- `compiler.version=17` (or your installed version, max 17)

#### 3. Build the C and Python API

Create a build directory and configure the project:

```bash
mkdir -p build
cd build
cmake ..
cmake --build .
```

This will build the required C and Python bindings. The build process may take several minutes.

#### 4. Install the Python package

From the root of the `hyperon-experimental` repository, install the Python package in editable mode:

```bash
pip install -e ./python[dev]
```

Or if you're installing from a different directory:

```bash
pip install -e /path/to/hyperon-experimental/python[dev]
```

### Verify Installation

You can verify both packages are installed correctly using several methods:

#### Method 1: Check installed packages

```bash
pip list | grep -E "(hyperon|supabase)"
```

You should see:
- `hyperon` (version 0.2.8 or later)
- `supabase` (version 2.25.0 or later)

#### Method 2: Test the MeTTa interpreter

The `metta-py` command should be available after installing hyperon:

```bash
metta-py --help
```

Or test with a simple MeTTa script:

```bash
echo '!(+ 1 1)' | metta-py
```

#### Method 3: Python import test

```bash
python -c "import supabase; print('✓ supabase installed')"
python -c "import hyperon; print('✓ hyperon installed')"
```

#### Method 4: Test metta-py command

```bash
metta-py --help
```

**Note:** `hyperon` is not a command-line tool - use `metta-py` instead to run MeTTa scripts.

### Fixing Import Issues

If you encounter `ModuleNotFoundError: No module named 'hyperon'` after installation, the virtual environment may need the hyperon path added to PYTHONPATH. This has been automatically configured in the activation script, but if you need to set it manually:

```bash
export PYTHONPATH="/path/to/hyperon-experimental/python:$PYTHONPATH"
```

Or add it to your virtual environment's `activate` script:

```bash
echo 'export PYTHONPATH="/path/to/hyperon-experimental/python:$PYTHONPATH"' >> .venv/bin/activate
```

### Troubleshooting

#### Conan compiler version errors

If you see errors like `Invalid setting '21' is not a valid 'settings.compiler.version' value`, update your Conan profile:

```bash
# Edit ~/.conan2/profiles/default
# Change compiler.version to a supported value (max 17 for apple-clang)
# Change compiler=clang to compiler=apple-clang (for macOS)
```

#### Build errors

- Ensure all prerequisites are installed and up to date
- Make sure Rust is in your PATH (`$HOME/.cargo/bin`)
- For macOS, ensure Xcode command line tools are installed: `xcode-select --install`

### References

- [Hyperon Experimental Repository](https://github.com/mvpeterson/hyperon-experimental)
- [Hyperon Installation Documentation](https://github.com/mvpeterson/hyperon-experimental/tree/main?tab=readme-ov-file#running-python-and-metta-examples)
- [Supabase Python Client](https://github.com/supabase/supabase-py)
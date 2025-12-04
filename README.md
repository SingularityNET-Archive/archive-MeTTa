# archive-MeTTa

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

You can verify both packages are installed correctly:

```bash
python -c "import hyperon; import supabase; print('✓ hyperon installed'); print('✓ supabase installed')"
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
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

## Usage

### Running the Script

1. Set up your environment variables in a `.env` file:
   ```bash
   DATABASE_URL=postgresql://user:password@host:port/dbname
   DB_PASSWORD=your_password
   ```

2. Run the script:
   ```bash
   python connect.py
   ```

The script will:
- Connect to your PostgreSQL database
- Load all tables and data into MeTTa
- Display atom types
- Run example queries

### Running Queries in Terminal

#### Option 1: Python Interactive Shell (REPL)

Start an interactive Python session and import the functions:

```bash
python
```

Then in the Python shell:

```python
# Import required modules
from hyperon import MeTTa
from connect import (
    load_all,
    query_by_id,
    query_batch,
    query_by_property_value,
    print_atom_types,
    list_atom_types,
    fetch_table,
    get_tables
)

# Initialize MeTTa interpreter
interp = MeTTa()

# Load all data (this may take a minute)
load_all(interp)

# Now you can run queries interactively:

# List atom types
print_atom_types(interp)

# Query a specific record
result = query_by_id(interp, "action_items", "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0", ["text", "assignee"])
print(result)

# Get a list of IDs from database
tables = get_tables()
if tables:
    sample_ids = [row["id"] for row in fetch_table(tables[0])[:5]]
    results = query_batch(interp, tables[0], sample_ids, ["text"])
    for r in results:
        print(r)
```

#### Option 2: Use the Example Query Scripts

**Main script:**
```bash
python query_examples.py
```

**Individual examples** (in `examples/` directory):
```bash
# List atom types
python examples/01_list_atom_types.py

# Query a specific record by ID
python examples/02_query_by_id.py

# Batch query multiple records
python examples/03_batch_query.py

# Query by property value (small result sets only)
python examples/04_query_property.py
```

Each example script is self-contained and demonstrates a specific query pattern. See `examples/README.md` for details.

#### Option 3: One-Liner Queries

For quick queries, you can use Python one-liners:

```bash
# List atom types
python -c "from hyperon import MeTTa; from connect import load_all, print_atom_types; interp = MeTTa(); load_all(interp); print_atom_types(interp)"

# Query a specific ID (replace with your ID)
python -c "from hyperon import MeTTa; from connect import load_all, query_by_id; interp = MeTTa(); load_all(interp); print(query_by_id(interp, 'action_items', 'e81d16b3-f53d-58f8-ace5-a2a78f0b21f0', ['text']))"
```

#### Option 4: Using MeTTa Directly

You can also use MeTTa's command-line interface:

```bash
# Start MeTTa REPL
metta-py
```

Then in MeTTa:

```metta
; Note: You'll need to load atoms first using Python, then you can query:
!(match &self (:action_items "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0") $result)
```

**Note:** For MeTTa REPL, you'll need to load atoms first using Python, as the atoms are loaded into the Python interpreter's space.

#### Quick Reference: Common Terminal Commands

```bash
# Start Python REPL
python

# Run a Python script
python query_examples.py

# Run with output to file
python query_examples.py > results.txt

# Run in background
python query_examples.py &

# Run with Python debugger
python -m pdb query_examples.py
```

### Recommended Production Pattern: SQL First, Then MeTTa

**In practice, you should almost always query your database first, then use MeTTa for the filtered results.**

Why?
- ✅ **SQL is fast** at filtering, joining, aggregating large datasets
- ✅ **Avoids MeTTa panics** by limiting result sets
- ✅ **Best performance** - use the right tool for each job
- ✅ **Scalable** - works with millions of records

**Pattern:**
```python
# Step 1: Use SQL to filter/limit (fast, no panics)
cursor.execute("""
    SELECT id FROM action_items 
    WHERE status = 'active' 
      AND assignee = 'John'
      AND due_date > NOW()
    LIMIT 100
""")
filtered_ids = [row[0] for row in cursor.fetchall()]

# Step 2: Query MeTTa for reasoning/pattern matching on filtered set
results = query_batch(interp, "action_items", filtered_ids, ["text", "assignee"])
```

**When to use each:**
- **Use SQL for:** Filtering, joins, aggregations, large scans, date ranges, text search
- **Use MeTTa for:** Pattern matching, reasoning, small result sets, knowledge graphs

### Query Examples

#### 1. List All Atom Types

```python
from connect import MeTTa, list_atom_types, print_atom_types

interp = MeTTa()
# ... load data ...

# Print human-readable list
# Note: Use verify_existence=False with large atom counts to avoid panics
print_atom_types(interp, verify_existence=False)

# Or get as data structure
types = list_atom_types(interp, verify_existence=False)
print(types['entity_types'])  # ['action_items', 'meetings', ...]
print(types['property_types']['action_items'])  # ['text', 'assignee', ...]
```

**Note:** With large atom counts (>100k), use `verify_existence=False` to avoid panics. The types are still accurate as they come from the database schema.

#### 2. Query a Specific Record by ID

```python
from connect import MeTTa, query_by_id

interp = MeTTa()
# ... load data ...

# Query a single record with specific properties
result = query_by_id(
    interp, 
    "action_items", 
    "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0",
    properties=["text", "assignee", "status"]
)

print(result)
# {
#   'id': 'e81d16b3-f53d-58f8-ace5-a2a78f0b21f0',
#   'text': 'Vani to approach DeepFunding...',
#   'assignee': 'CallyFromAuron',
#   'status': 'active'
# }
```

#### 3. Query Multiple Records (Batch Processing)

```python
from connect import MeTTa, query_batch

interp = MeTTa()
# ... load data ...

# Get IDs from database first (hybrid approach)
ids = ["id1", "id2", "id3", "id4", "id5"]

# Query in batches (safe for large lists)
results = query_batch(
    interp,
    "action_items",
    ids,
    properties=["text", "assignee"],
    batch_size=50  # Process 50 at a time
)

for result in results:
    print(f"{result['id']}: {result.get('text', 'N/A')}")
```

#### 4. Direct MeTTa Query Syntax

You can also use MeTTa queries directly:

```python
from hyperon import MeTTa

interp = MeTTa()
# ... load data ...

# Check if a record exists
query = '!(match &self (:action_items "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0") $result)'
results = interp.run(query)
print(results)  # [[$result]] means it exists

# Extract a property value
query = '!(match &self (:action_items.text "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0" $val) $val)'
results = interp.run(query)
print(results)  # [["Vani to approach DeepFunding..."]]
```

#### 5. Hybrid Approach: SQL + MeTTa

For production use, combine SQL filtering with MeTTa queries:

```python
from connect import MeTTa, query_batch, fetch_table

interp = MeTTa()
# ... load data ...

# Step 1: Use SQL to filter/limit (fast, no panics)
cursor.execute("""
    SELECT id FROM action_items 
    WHERE status = 'active' 
    LIMIT 100
""")
filtered_ids = [row[0] for row in cursor.fetchall()]

# Step 2: Query MeTTa for filtered IDs only
results = query_batch(
    interp,
    "action_items",
    filtered_ids,
    properties=["text", "assignee"]
)

# Now you have filtered data from MeTTa
for result in results:
    print(f"{result['assignee']}: {result['text']}")
```

#### 6. Find Records by Property Value

**⚠️ Warning:** Only use for small result sets (<1000 matches):

```python
from connect import MeTTa, query_by_property_value

interp = MeTTa()
# ... load data ...

# Find all action items assigned to a specific person
ids = query_by_property_value(
    interp,
    "action_items",
    "assignee",
    "CallyFromAuron"
)

print(f"Found {len(ids)} action items")
# For large result sets, use SQL instead:
# SELECT id FROM action_items WHERE assignee = 'CallyFromAuron'
```

### Production Best Practices

#### ✅ Recommended: SQL First, Then MeTTa (Hybrid Approach)

**This is the recommended pattern for production:**

```python
from connect import query_batch, cursor

# Step 1: Use SQL to filter/limit (fast, handles millions of records)
cursor.execute("""
    SELECT id FROM action_items 
    WHERE status = 'active' 
      AND assignee = %s
      AND due_date > NOW()
    ORDER BY due_date ASC
    LIMIT 100
""", ("John",))
filtered_ids = [row[0] for row in cursor.fetchall()]

# Step 2: Use MeTTa for reasoning on filtered set (small, safe)
results = query_batch(
    interp, 
    "action_items", 
    filtered_ids, 
    ["text", "assignee", "status"],
    batch_size=50
)

# Now you have filtered data from MeTTa for further processing
for result in results:
    # Do reasoning, pattern matching, etc.
    print(f"{result['assignee']}: {result['text']}")
```

**Benefits:**
- ✅ Fast: SQL handles filtering efficiently
- ✅ Safe: Small result sets avoid MeTTa panics
- ✅ Scalable: Works with millions of records
- ✅ Flexible: Use SQL for what it's good at, MeTTa for reasoning

#### ✅ Alternative Safe Patterns

1. **Query by specific ID** - Always safe
   ```python
   result = query_by_id(interp, "table", "specific-id")
   ```

2. **Batch processing** - Safe for multiple IDs (when you already have the IDs)
   ```python
   results = query_batch(interp, "table", ids, batch_size=50)
   ```

#### ❌ Avoid These (Causes Panics)

1. **Variable queries with large result sets**
   ```python
   # DON'T: This will panic with >10k results
   query = '!(match &self (:action_items $id) $id)'
   ```

2. **get_atoms() or atom_count()** - Panics with large spaces
   ```python
   # DON'T: Will panic
   atoms = space.get_atoms()
   count = space.atom_count()
   ```

3. **Unfiltered property queries** - Use SQL first
   ```python
   # DON'T: Use SQL instead
   ids = query_by_property_value(interp, "table", "prop", "value")
   # DO: Use SQL
   cursor.execute("SELECT id FROM table WHERE prop = %s", (value,))
   ```

### Atom Type Structure

Atoms are stored in two formats:

1. **Entity atoms**: `(:table_name id_value)`
   - Example: `(:action_items "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0")`
   - Represents: "This ID exists in the action_items table"

2. **Property atoms**: `(:table_name.property_name id_value property_value)`
   - Example: `(:action_items.text "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0" "Task description")`
   - Represents: "The 'text' property of this action_item has this value"

### Understanding the Atom Types Output

When you run `print_atom_types()`, you see output like:

```
Entity Types (from database schema):
  • :action_items
    Properties: :action_items.agenda_item_id, :action_items.text, :action_items.assignee, ...
```

**What this means:**

1. **Entity Types** (e.g., `:action_items`, `:meetings`)
   - These are your database **table names**
   - Each table becomes an entity type in MeTTa
   - You can query: `(:action_items $id)` to find all action item IDs

2. **Properties** (e.g., `:action_items.text`, `:action_items.assignee`)
   - These are your database **column names**
   - Format: `:table_name.column_name`
   - You can query: `(:action_items.text $id $value)` to find text values

3. **The `...` notation**
   - Means "and more properties" (output is truncated for readability)
   - Example: `... and 4 more properties` means there are 4 additional columns not shown

4. **Example mapping:**
   ```
   Database Table: action_items
   Columns: id, text, assignee, status, due_date
   
   Becomes in MeTTa:
   - Entity type: :action_items
   - Properties: 
     • :action_items.text
     • :action_items.assignee
     • :action_items.status
     • :action_items.due_date
   ```

5. **How to use this information:**
   - To query a specific record: Use the entity type with an ID
   - To get a property value: Use the property type with an ID
   - Example queries:
     ```python
     # Check if record exists
     query = '!(match &self (:action_items "some-id") $result)'
     
     # Get the text property
     query = '!(match &self (:action_items.text "some-id" $val) $val)'
     ```

### Complete Example Script

```python
#!/usr/bin/env python3
from hyperon import MeTTa
from connect import (
    load_all, 
    query_by_id, 
    query_batch, 
    print_atom_types,
    fetch_table
)

# Initialize
interp = MeTTa()

# Load data
print("Loading data...")
load_all(interp)

# List available atom types
print("\nAvailable atom types:")
print_atom_types(interp)

# Query a specific record
print("\nQuerying specific record:")
result = query_by_id(
    interp,
    "action_items",
    "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0",
    properties=["text", "assignee"]
)
print(result)

# Batch query
print("\nBatch querying:")
sample_ids = [row["id"] for row in fetch_table("action_items")[:5]]
results = query_batch(interp, "action_items", sample_ids, ["text"])
for r in results:
    print(f"  {r['id']}: {r.get('text', 'N/A')[:50]}...")
```

### References

- [Hyperon Experimental Repository](https://github.com/mvpeterson/hyperon-experimental)
- [Hyperon Installation Documentation](https://github.com/mvpeterson/hyperon-experimental/tree/main?tab=readme-ov-file#running-python-and-metta-examples)
- [Supabase Python Client](https://github.com/supabase/supabase-py)
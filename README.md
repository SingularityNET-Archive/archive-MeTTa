# archive-MeTTa

A Python toolkit for loading PostgreSQL/Supabase data into MeTTa (Meta Type Talk) knowledge representation space, enabling pattern matching and reasoning on your database.

## Overview

This project provides a bridge between PostgreSQL databases and MeTTa, allowing you to:

- **Load database tables** into MeTTa as structured atoms
- **Query data** using MeTTa's pattern matching and reasoning capabilities
- **Combine SQL and MeTTa** for optimal performance (recommended hybrid approach)

### Recommended Approach: SQL First, Then MeTTa

**For production use, always query your database first, then pass filtered results to MeTTa.**

This hybrid approach gives you:
- ✅ **Fast filtering** - SQL handles millions of records efficiently
- ✅ **No panics** - Small result sets avoid MeTTa limitations
- ✅ **Best performance** - Right tool for each job
- ✅ **Scalable** - Works with large datasets

**Pattern:**
```python
# Step 1: SQL filters/limits (fast)
cursor.execute("SELECT id FROM table WHERE condition LIMIT 100")
ids = [row[0] for row in cursor.fetchall()]

# Step 2: MeTTa queries filtered set (safe)
results = query_batch(interp, "table", ids, ["text", "assignee"])
```

---

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (see Installation section below)
pip install supabase python-dotenv psycopg2
```

### 2. Configure Database Connection

Create a `.env` file:
```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
DB_PASSWORD=your_password
```

### 3. Run Examples

```bash
# List available atom types (no data loading needed)
python examples/01_list_atom_types.py

# Query a specific record
python examples/02_query_by_id.py

# Batch query multiple records
python examples/03_batch_query.py

# Hybrid SQL + MeTTa approach (recommended)
python examples/05_hybrid_sql_metta.py
```

---

## Example Outputs

### Example 1: List Atom Types

**Command:**
```bash
python examples/01_list_atom_types.py
```

**Output:**
```
============================================================
Example 1: List Atom Types
============================================================
Using hybrid approach: SQL schema → Atom types

Step 1: Getting atom types from database schema...
  Querying: information_schema.tables and information_schema.columns
  ✓ Found 12 entity types

============================================================
ATOM TYPES IN DATABASE SCHEMA
============================================================

  • :action_items
    Properties: :action_items.agenda_item_id, :action_items.text, 
                :action_items.assignee, :action_items.due_date, 
                :action_items.status, :action_items.raw_json, ...
    ... and 2 more properties

  • :meetings
    Properties: :meetings.workgroup_id, :meetings.date, :meetings.type, 
                :meetings.host, :meetings.documenter, ...
    ... and 4 more properties

  • :agenda_items
    Properties: :agenda_items.meeting_id, :agenda_items.status, ...
```

### Example 2: Query Specific Record

**Command:**
```bash
python examples/02_query_by_id.py
```

**Output:**
```
============================================================
Example 2: Query Specific Record by ID
============================================================
Using hybrid approach: SQL → MeTTa

Step 1: Using SQL to get a sample ID from 'action_items'...
  ✓ Found ID: e81d16b3-f53d-58f8-ace5-a2a78f0b21f0

Step 2: Querying MeTTa for this ID...
  Table: action_items
  ✓ Retrieved from MeTTa:

    id                   = e81d16b3-f53d-58f8-ace5-a2a78f0b21f0
    text                 = Vani to approach DeepFunding, to ask about the issue rai...
    assignee             = CallyFromAuron
    status               = active
```

### Example 3: Batch Query

**Command:**
```bash
python examples/03_batch_query.py
```

**Output:**
```
============================================================
Example 3: Batch Query Multiple Records
============================================================
Using hybrid approach: SQL → MeTTa

Step 1: Using SQL to get filtered IDs from 'action_items'...
  Query: SELECT id FROM table LIMIT 5
  ✓ Found 5 IDs using SQL

Step 2: Querying MeTTa for 5 records...
  Using batch size: 10
  ✓ Retrieved 5 records from MeTTa

Results:
  1. abc123...: Vani to approach DeepFunding, to ask about...
  2. def456...: Review quarterly budget and prepare report...
  3. ghi789...: Schedule team meeting for next sprint...
  4. jkl012...: Update documentation for new API endpoints...
  5. mno345...: Follow up with client on project proposal...
```

### Example 5: Hybrid SQL + MeTTa (Recommended)

**Command:**
```bash
python examples/05_hybrid_sql_metta.py
```

**Output:**
```
============================================================
Example 5: Hybrid SQL + MeTTa Approach
============================================================
Recommended pattern for production use

Loading data into MeTTa...
Loading table: action_items (4081 rows)
Loading table: agenda_items (1431 rows)
...
✓ Loaded 119678 atoms into MeTTa

Step 1: Using SQL to filter records...
  Query: SELECT id FROM action_items WHERE status = 'active' LIMIT 10
  ✓ Found 10 records using SQL

Step 2: Querying MeTTa for filtered IDs...
  Querying 10 records from MeTTa...
  ✓ Retrieved 10 records from MeTTa

Step 3: Processing results...
  1. [active] CallyFromAuron: Vani to approach DeepFunding...
  2. [active] JohnDoe: Review quarterly budget...
  3. [active] JaneSmith: Schedule team meeting...
  ...

============================================================
Why This Approach?
============================================================

✅ SQL is fast at filtering large datasets
✅ Avoids MeTTa panics by limiting result sets  
✅ Best performance - use the right tool for each job
✅ Scalable - works with millions of records
✅ Flexible - SQL for filtering, MeTTa for reasoning
```

---

## Installation

### Prerequisites

- Python 3.8 or later
- pip (23.1.2 or later)
- Rust (latest stable version) - [Install Rust](https://www.rust-lang.org/tools/install)
- CMake (3.24 or later)
- GCC (7.5 or later) or equivalent C/C++ compiler
- Conan (C++ package manager)

### Python Environment Setup

#### 1. Create Virtual Environment

```bash
cd /path/to/archive-MeTTa
python3 -m venv .venv
```

#### 2. Activate Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

After activation, your terminal prompt should show `(.venv)`.

#### 3. Upgrade pip

```bash
pip install --upgrade pip
```

### Installing Dependencies

#### Install Supabase and Other Python Packages

```bash
pip install supabase python-dotenv psycopg2-binary
```

#### Install Hyperon (from source)

Hyperon is not available on PyPI and must be installed from source:

**1. Clone the hyperon-experimental repository:**
```bash
cd /path/to/your/projects
git clone https://github.com/mvpeterson/hyperon-experimental.git
cd hyperon-experimental
```

**2. Install build prerequisites:**

Install `cbindgen`:
```bash
cargo install --force cbindgen
```

Install `conan`:
```bash
pip install conan==2.19.1
conan profile detect --force
```

**Note for macOS users:** If you encounter compiler version errors, edit `~/.conan2/profiles/default` and ensure:
- `compiler=apple-clang`
- `compiler.version=17` (or your installed version, max 17)

**3. Build the C and Python API:**
```bash
mkdir -p build
cd build
cmake ..
cmake --build .
```

**4. Install the Python package:**
```bash
# From hyperon-experimental root directory
pip install -e ./python[dev]
```

**5. Configure PYTHONPATH:**

Add to `.venv/bin/activate`:
```bash
echo 'export PYTHONPATH="/path/to/hyperon-experimental/python:$PYTHONPATH"' >> .venv/bin/activate
```

Replace `/path/to/hyperon-experimental` with the actual path.

### Verify Installation

```bash
# Check packages
pip list | grep -E "(hyperon|supabase)"

# Test imports
python -c "import hyperon; print('✓ hyperon installed')"
python -c "import supabase; print('✓ supabase installed')"

# Test MeTTa
echo '!(+ 1 1)' | metta-py
```

---

## Usage

### Running the Main Script

1. Set up your `.env` file with database credentials
2. Run:
   ```bash
   python connect.py
   ```

The script will:
- Connect to your PostgreSQL database
- Load all tables and data into MeTTa
- Display atom types
- Run example queries

### Running Individual Examples

Each example demonstrates a specific pattern:

```bash
# List atom types (no data loading)
python examples/01_list_atom_types.py

# Query specific record
python examples/02_query_by_id.py

# Batch query
python examples/03_batch_query.py

# Query by property (uses SQL filtering)
python examples/04_query_property.py

# Hybrid approach (recommended)
python examples/05_hybrid_sql_metta.py
```

### Using Python REPL

```python
from hyperon import MeTTa
from connect import load_all, query_by_id, query_batch, cursor

# Initialize
interp = MeTTa()
load_all(interp)

# Hybrid approach: SQL → MeTTa
cursor.execute("SELECT id FROM action_items WHERE status = 'active' LIMIT 10")
ids = [row[0] for row in cursor.fetchall()]

results = query_batch(interp, "action_items", ids, ["text", "assignee"])
for r in results:
    print(f"{r['assignee']}: {r['text']}")
```

---

## Query Patterns

### 1. List Atom Types

Get types directly from database schema (no MeTTa loading needed):

```python
from connect import list_atom_types

types = list_atom_types(None, verify_existence=False)
print(types['entity_types'])  # ['action_items', 'meetings', ...]
```

### 2. Query by Specific ID

```python
from connect import query_by_id

result = query_by_id(
    interp, 
    "action_items", 
    "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0",
    properties=["text", "assignee", "status"]
)
```

### 3. Batch Query (Hybrid Approach)

```python
from connect import query_batch, cursor

# Step 1: SQL filters
cursor.execute("SELECT id FROM action_items WHERE status = 'active' LIMIT 100")
ids = [row[0] for row in cursor.fetchall()]

# Step 2: MeTTa queries
results = query_batch(interp, "action_items", ids, ["text", "assignee"])
```

### 4. Query by Property Value

**Recommended:** Use SQL for filtering:

```python
from connect import query_batch, cursor

# SQL finds matching IDs
cursor.execute("SELECT id FROM action_items WHERE assignee = %s", ("John",))
ids = [row[0] for row in cursor.fetchall()]

# MeTTa queries those IDs
results = query_batch(interp, "action_items", ids, ["text"])
```

---

## Production Best Practices

### ✅ Recommended: Hybrid SQL + MeTTa

**Always use this pattern for production:**

```python
from connect import query_batch, cursor

# Step 1: SQL filters/limits (fast, handles millions)
cursor.execute("""
    SELECT id FROM action_items 
    WHERE status = 'active' 
      AND assignee = %s
      AND due_date > NOW()
    ORDER BY due_date ASC
    LIMIT 100
""", ("John",))
filtered_ids = [row[0] for row in cursor.fetchall()]

# Step 2: MeTTa for reasoning (small, safe)
results = query_batch(
    interp, 
    "action_items", 
    filtered_ids, 
    ["text", "assignee", "status"],
    batch_size=50
)
```

**Benefits:**
- ✅ Fast: SQL handles filtering efficiently
- ✅ Safe: Small result sets avoid MeTTa panics
- ✅ Scalable: Works with millions of records
- ✅ Flexible: SQL for filtering, MeTTa for reasoning

### ✅ Safe Patterns

1. **Query by specific ID** - Always safe
   ```python
   result = query_by_id(interp, "table", "specific-id")
   ```

2. **Batch processing** - Safe for multiple IDs
   ```python
   results = query_batch(interp, "table", ids, batch_size=50)
   ```

### ❌ Avoid These (Causes Panics)

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

---

## Understanding Atom Types

### Atom Structure

Atoms are stored in two formats:

1. **Entity atoms**: `(:table_name id_value)`
   - Example: `(:action_items "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0")`
   - Represents: "This ID exists in the action_items table"

2. **Property atoms**: `(:table_name.property_name id_value property_value)`
   - Example: `(:action_items.text "e81d16b3-f53d-58f8-ace5-a2a78f0b21f0" "Task description")`
   - Represents: "The 'text' property of this action_item has this value"

### Database to MeTTa Mapping

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

### Querying Atoms

```python
# Check if record exists
query = '!(match &self (:action_items "some-id") $result)'

# Get a property value
query = '!(match &self (:action_items.text "some-id" $val) $val)'
```

---

## Troubleshooting

### Conan Compiler Version Errors

If you see errors like `Invalid setting '21' is not a valid 'settings.compiler.version' value`:

```bash
# Edit ~/.conan2/profiles/default
# Change compiler.version to a supported value (max 17 for apple-clang)
# Change compiler=clang to compiler=apple-clang (for macOS)
```

### Build Errors

- Ensure all prerequisites are installed and up to date
- Make sure Rust is in your PATH (`$HOME/.cargo/bin`)
- For macOS, ensure Xcode command line tools: `xcode-select --install`

### Import Issues

If you encounter `ModuleNotFoundError: No module named 'hyperon'`:

```bash
export PYTHONPATH="/path/to/hyperon-experimental/python:$PYTHONPATH"
```

Or add to `.venv/bin/activate`:
```bash
echo 'export PYTHONPATH="/path/to/hyperon-experimental/python:$PYTHONPATH"' >> .venv/bin/activate
```

### Query Panics

If queries cause panics:
- Use SQL to filter first, then query MeTTa
- Limit result sets to <10k records
- Avoid `get_atoms()` or `atom_count()` with large spaces
- Use `verify_existence=False` when listing atom types

---

## References

- [Hyperon Experimental Repository](https://github.com/mvpeterson/hyperon-experimental)
- [Hyperon Installation Documentation](https://github.com/mvpeterson/hyperon-experimental/tree/main?tab=readme-ov-file#running-python-and-metta-examples)
- [Supabase Python Client](https://github.com/supabase/supabase-py)

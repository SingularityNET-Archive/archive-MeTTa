# Query Examples

This directory contains individual example scripts demonstrating different MeTTa query patterns.

## Running Examples

Each example can be run independently:

```bash
# List atom types
python examples/01_list_atom_types.py

# Query a specific record by ID
python examples/02_query_by_id.py

# Batch query multiple records
python examples/03_batch_query.py

# Query by property value (small result sets only)
python examples/04_query_property.py

# Hybrid SQL + MeTTa (RECOMMENDED for production)
python examples/05_hybrid_sql_metta.py
```

## Example Descriptions

### 01_list_atom_types.py
Lists all atom types available in the MeTTa space. Shows entity types (tables) and their properties.

### 02_query_by_id.py
Demonstrates querying a specific record by its ID. Shows how to extract property values safely.

### 03_batch_query.py
Shows how to query multiple records efficiently using batch processing. Safe for large lists of IDs.

### 04_query_property.py
Demonstrates finding records by property value. **Warning:** Only use for small result sets (<1000 matches).

### 05_hybrid_sql_metta.py ⭐ **RECOMMENDED**
Demonstrates the **recommended production pattern**: Use SQL to filter/limit large datasets, then pass filtered IDs to MeTTa for reasoning. This is the best approach for production use.

## Notes

- Each script loads data independently. If you're running multiple examples in the same session, you can comment out `load_all()` after the first run.
- Some queries may cause panics with large atom counts. The examples use safe patterns to avoid this.
- For production use, prefer the hybrid SQL + MeTTa approach shown in the main README.


#!/usr/bin/env python3
"""
Main query examples script.

This script runs all example queries. For individual examples,
see the files in the examples/ directory:
  - examples/01_list_atom_types.py
  - examples/02_query_by_id.py
  - examples/03_batch_query.py
  - examples/04_query_property.py
"""

import sys
import os

# Add parent directory to path so we can import connect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hyperon import MeTTa
from connect import (
    load_all,
    query_by_id,
    query_batch,
    print_atom_types,
    fetch_table,
    get_tables
)

def main():
    print("=" * 60)
    print("MeTTa Query Examples")
    print("=" * 60)
    print("\nThis script demonstrates basic query patterns.")
    print("For individual examples, see the examples/ directory.\n")
    
    # Initialize MeTTa interpreter
    interp = MeTTa()
    
    # Load data (only needed once per session)
    print("Loading data into MeTTa...")
    load_all(interp)
    print("Data loaded!\n")
    
    # Get available tables
    tables = get_tables()
    if not tables:
        print("No tables found in database.")
        return
    
    first_table = tables[0]
    print(f"Using table: {first_table}\n")
    
    # Example 1: List atom types
    print("=" * 60)
    print("Example 1: List Atom Types")
    print("=" * 60)
    try:
        print_atom_types(interp, verify_existence=False)
    except Exception as e:
        print(f"Note: Could not list atom types (error: {e})")
        print("This is expected with large atom counts. Types are available from schema.")
    
    # Example 2: Query a specific record (with error handling)
    print("\n" + "=" * 60)
    print("Example 2: Query Specific Record by ID")
    print("=" * 60)
    sample_rows = fetch_table(first_table)[:1]
    if sample_rows and sample_rows[0].get("id"):
        sample_id = sample_rows[0]["id"]
        print(f"Querying record ID: {sample_id}")
        
        # Use only safe properties to avoid panics
        safe_properties = ["text", "assignee", "status"]
        
        try:
            result = query_by_id(interp, first_table, sample_id, safe_properties)
            if result:
                print("\nResult:")
                for key, value in result.items():
                    display_value = str(value)
                    if len(display_value) > 80:
                        display_value = display_value[:77] + "..."
                    print(f"  {key:20s} = {display_value}")
            else:
                print("  Record not found")
        except Exception as e:
            print(f"  Error querying record: {e}")
            print("  Some property queries may cause panics with large atom counts")
    
    # Example 3: Batch query (safe)
    print("\n" + "=" * 60)
    print("Example 3: Batch Query Multiple Records")
    print("=" * 60)
    try:
        sample_ids = [row["id"] for row in fetch_table(first_table)[:3]]  # Reduced to 3
        print(f"Querying {len(sample_ids)} records...")
        
        results = query_batch(interp, first_table, sample_ids, ["text"], batch_size=10)
        print(f"\nRetrieved {len(results)} records:")
        for i, r in enumerate(results, 1):
            text = r.get('text', 'N/A')
            if len(text) > 60:
                text = text[:57] + "..."
            print(f"  {i}. {r['id']}: {text}")
    except Exception as e:
        print(f"Error in batch query: {e}")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
    print("\nFor more examples, see:")
    print("  python examples/01_list_atom_types.py")
    print("  python examples/02_query_by_id.py")
    print("  python examples/03_batch_query.py")
    print("  python examples/04_query_property.py")

if __name__ == "__main__":
    main()


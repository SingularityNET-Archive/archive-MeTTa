#!/usr/bin/env python3
"""
Example 3: Batch Query Multiple Records

This script demonstrates how to query multiple records in batches.
"""

from hyperon import MeTTa
from connect import load_all, query_batch, fetch_table, get_tables

def main():
    print("=" * 60)
    print("Example 3: Batch Query Multiple Records")
    print("=" * 60)
    
    # Initialize MeTTa interpreter
    interp = MeTTa()
    
    # Load data
    print("\nLoading data into MeTTa...")
    load_all(interp)
    print("Data loaded!\n")
    
    # Get sample IDs
    tables = get_tables()
    if not tables:
        print("No tables found.")
        return
    
    first_table = tables[0]
    sample_ids = [row["id"] for row in fetch_table(first_table)[:5]]
    
    print(f"Querying {len(sample_ids)} records from '{first_table}'...")
    print(f"Using batch size: 10\n")
    
    # Query with safe property
    results = query_batch(interp, first_table, sample_ids, ["text"], batch_size=10)
    
    print(f"Retrieved {len(results)} records:")
    for i, r in enumerate(results, 1):
        text = r.get('text', 'N/A')
        if len(text) > 60:
            text = text[:57] + "..."
        print(f"  {i}. {r['id']}: {text}")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()


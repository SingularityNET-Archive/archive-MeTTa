#!/usr/bin/env python3
"""
Example 3: Batch Query Multiple Records

This script demonstrates the hybrid approach:
1. Use SQL to filter/limit records
2. Pass filtered IDs to MeTTa for batch querying
"""

from hyperon import MeTTa
from connect import load_all, query_batch, cursor, get_tables

def main():
    print("=" * 60)
    print("Example 3: Batch Query Multiple Records")
    print("=" * 60)
    print("Using hybrid approach: SQL → MeTTa\n")
    
    # Initialize MeTTa interpreter
    interp = MeTTa()
    
    # Load data
    print("Loading data into MeTTa...")
    load_all(interp)
    print("Data loaded!\n")
    
    # Get tables
    tables = get_tables()
    if not tables:
        print("No tables found.")
        return
    
    first_table = tables[0]
    
    # Step 1: Use SQL to filter/limit (fast, handles large datasets)
    print(f"Step 1: Using SQL to get filtered IDs from '{first_table}'...")
    print("  Query: SELECT id FROM table LIMIT 5")
    
    try:
        cursor.execute(f"SELECT id FROM {first_table} LIMIT 5")
        sample_ids = [row[0] for row in cursor.fetchall()]
        print(f"  ✓ Found {len(sample_ids)} IDs using SQL\n")
        
        if sample_ids:
            # Step 2: Use MeTTa for batch querying (small, safe)
            print(f"Step 2: Querying MeTTa for {len(sample_ids)} records...")
            print(f"  Using batch size: 10")
            
            results = query_batch(interp, first_table, sample_ids, ["text"], batch_size=10)
            
            print(f"  ✓ Retrieved {len(results)} records from MeTTa\n")
            
            # Display results
            print("Results:")
            for i, r in enumerate(results, 1):
                text = r.get('text', 'N/A')
                if len(text) > 60:
                    text = text[:57] + "..."
                print(f"  {i}. {r['id']}: {text}")
        else:
            print("  No records found")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("Why this approach?")
    print("=" * 60)
    print("""
✅ SQL handles filtering efficiently (millions of records)
✅ MeTTa processes small, filtered batches safely
✅ Avoids panics by limiting result sets
✅ Best performance - right tool for each job
✅ Production-ready pattern
    """)
    
    print("=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()


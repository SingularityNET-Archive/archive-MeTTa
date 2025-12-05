#!/usr/bin/env python3
"""
Example 4: Query by Property Value (Hybrid Approach)

This script demonstrates the RECOMMENDED approach:
Use SQL to find records by property value, then query MeTTa for those IDs.

This is much safer and faster than using MeTTa's query_by_property_value.
"""

from hyperon import MeTTa
from connect import load_all, query_batch, cursor, get_tables

def main():
    print("=" * 60)
    print("Example 4: Query by Property Value")
    print("=" * 60)
    print("Using hybrid approach: SQL for filtering → MeTTa for results\n")
    
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
    
    # Step 1: Use SQL to find records by property value (fast, safe)
    print(f"Step 1: Using SQL to find records by property value...")
    print(f"  Table: {first_table}")
    
    # Try to find a property we can search on
    # First, get a sample value
    try:
        cursor.execute(f"SELECT assignee, status FROM {first_table} WHERE assignee IS NOT NULL LIMIT 1")
        sample = cursor.fetchone()
        
        if sample and sample[0]:
            search_prop = "assignee"
            search_value = sample[0]
            
            print(f"  Searching for: {search_prop} = '{search_value}'")
            print(f"  Query: SELECT id FROM {first_table} WHERE {search_prop} = %s LIMIT 10")
            
            # Use SQL to find matching IDs (fast, handles large datasets)
            cursor.execute(
                f"SELECT id FROM {first_table} WHERE {search_prop} = %s LIMIT 10",
                (search_value,)
            )
            matching_ids = [row[0] for row in cursor.fetchall()]
            print(f"  ✓ Found {len(matching_ids)} matching IDs using SQL\n")
            
            if matching_ids:
                # Step 2: Query MeTTa for those IDs (small, safe)
                print(f"Step 2: Querying MeTTa for {len(matching_ids)} records...")
                
                results = query_batch(
                    interp,
                    first_table,
                    matching_ids,
                    ["text", "assignee", "status"],
                    batch_size=10
                )
                
                print(f"  ✓ Retrieved {len(results)} records from MeTTa\n")
                
                # Display results
                print("Results:")
                for i, r in enumerate(results, 1):
                    text = r.get('text', 'N/A')
                    if len(text) > 50:
                        text = text[:47] + "..."
                    print(f"  {i}. [{r.get('status', 'N/A')}] {r.get('assignee', 'N/A')}: {text}")
            else:
                print("  No matching records found")
        else:
            print("  No suitable sample value found")
            print("  Try modifying the SQL query to search for a specific property value")
            
    except Exception as e:
        print(f"  Error: {e}")
        print("  This may happen if the table structure is different")
    
    print("\n" + "=" * 60)
    print("Why use SQL instead of MeTTa for filtering?")
    print("=" * 60)
    print("""
✅ SQL is MUCH faster for filtering (indexed, optimized)
✅ Handles millions of records efficiently
✅ Avoids MeTTa panics with large result sets
✅ Can use complex WHERE clauses, joins, aggregations
✅ Production-ready and scalable

❌ MeTTa's query_by_property_value:
   - Slow with large datasets
   - Can cause panics with >1000 matches
   - Not optimized for filtering
   - Use only for very small result sets

RECOMMENDED: Always use SQL for filtering, MeTTa for reasoning
    """)
    
    print("=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()


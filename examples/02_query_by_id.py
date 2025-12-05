#!/usr/bin/env python3
"""
Example 2: Query Specific Record by ID

This script demonstrates how to query a specific record by its ID.
Uses the hybrid approach: SQL to get the ID, then MeTTa to query it.
"""

from hyperon import MeTTa
from connect import load_all, query_by_id, cursor, get_tables

def main():
    print("=" * 60)
    print("Example 2: Query Specific Record by ID")
    print("=" * 60)
    print("Using hybrid approach: SQL → MeTTa\n")
    
    # Initialize MeTTa interpreter
    interp = MeTTa()
    
    # Load data
    print("Loading data into MeTTa...")
    load_all(interp)
    print("Data loaded!\n")
    
    # Get a sample ID using SQL (fast, no panics)
    tables = get_tables()
    if not tables:
        print("No tables found.")
        return
    
    first_table = tables[0]
    print(f"Step 1: Using SQL to get a sample ID from '{first_table}'...")
    
    try:
        cursor.execute(f"SELECT id FROM {first_table} LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            sample_id = row[0]
            print(f"  ✓ Found ID: {sample_id}\n")
            
            print(f"Step 2: Querying MeTTa for this ID...")
            print(f"  Table: {first_table}")
            
            # Query with safe properties only (to avoid panics)
            safe_properties = ["text", "assignee", "status", "title", "name"]
            
            result = query_by_id(interp, first_table, sample_id, safe_properties)
            
            if result:
                print("  ✓ Retrieved from MeTTa:\n")
                for key, value in result.items():
                    display_value = str(value)
                    if len(display_value) > 80:
                        display_value = display_value[:77] + "..."
                    print(f"    {key:20s} = {display_value}")
            else:
                print("  Record not found in MeTTa space")
        else:
            print("  No records found in table")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("Why this approach?")
    print("=" * 60)
    print("""
✅ SQL is fast for finding IDs
✅ MeTTa handles the actual query safely
✅ Avoids loading all data just to find one ID
✅ Scalable pattern for production
    """)
    
    print("=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()


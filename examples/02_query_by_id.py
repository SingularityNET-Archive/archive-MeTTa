#!/usr/bin/env python3
"""
Example 2: Query Specific Record by ID

This script demonstrates how to query a specific record by its ID.
"""

from hyperon import MeTTa
from connect import load_all, query_by_id, fetch_table, get_tables

def main():
    print("=" * 60)
    print("Example 2: Query Specific Record by ID")
    print("=" * 60)
    
    # Initialize MeTTa interpreter
    interp = MeTTa()
    
    # Load data
    print("\nLoading data into MeTTa...")
    load_all(interp)
    print("Data loaded!\n")
    
    # Get a sample ID
    tables = get_tables()
    if not tables:
        print("No tables found.")
        return
    
    first_table = tables[0]
    sample_rows = fetch_table(first_table)[:1]
    
    if sample_rows and sample_rows[0].get("id"):
        sample_id = sample_rows[0]["id"]
        print(f"Querying record ID: {sample_id}")
        print(f"Table: {first_table}\n")
        
        # Query with safe properties only (to avoid panics)
        # Use common property names that are less likely to cause issues
        safe_properties = ["text", "assignee", "status", "title", "name"]
        
        result = query_by_id(interp, first_table, sample_id, safe_properties)
        
        if result:
            print("Result:")
            for key, value in result.items():
                display_value = str(value)
                if len(display_value) > 80:
                    display_value = display_value[:77] + "..."
                print(f"  {key:20s} = {display_value}")
        else:
            print("  Record not found")
    else:
        print("No sample record found")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()


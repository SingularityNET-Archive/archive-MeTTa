#!/usr/bin/env python3
"""
Example 4: Query by Property Value

This script demonstrates how to find records by property value.
WARNING: Only use for small result sets (<1000 matches).
"""

from hyperon import MeTTa
from connect import load_all, query_by_property_value, fetch_table, get_tables

def main():
    print("=" * 60)
    print("Example 4: Query by Property Value")
    print("=" * 60)
    print("WARNING: Only use for small result sets (<1000 matches)")
    print("=" * 60)
    
    # Initialize MeTTa interpreter
    interp = MeTTa()
    
    # Load data
    print("\nLoading data into MeTTa...")
    load_all(interp)
    print("Data loaded!\n")
    
    # Get a sample value from the database
    tables = get_tables()
    if not tables:
        print("No tables found.")
        return
    
    first_table = tables[0]
    sample_rows = fetch_table(first_table)[:1]
    
    if sample_rows and sample_rows[0].get("id"):
        # Try to find a property with a value we can search for
        sample_row = sample_rows[0]
        
        # Look for a property that might have multiple matches
        # Try "assignee" or "status" if available
        search_prop = None
        search_value = None
        
        for prop in ["assignee", "status", "type"]:
            if prop in sample_row and sample_row[prop]:
                search_prop = prop
                search_value = sample_row[prop]
                break
        
        if search_prop and search_value:
            print(f"Searching for records where {search_prop} = '{search_value}'")
            print(f"Table: {first_table}\n")
            
            try:
                ids = query_by_property_value(interp, first_table, search_prop, search_value)
                print(f"Found {len(ids)} matching records")
                if ids:
                    print(f"First 5 IDs:")
                    for i, record_id in enumerate(ids[:5], 1):
                        print(f"  {i}. {record_id}")
                    if len(ids) > 5:
                        print(f"  ... and {len(ids) - 5} more")
            except Exception as e:
                print(f"Error: {e}")
                print("This may happen if there are too many matches or the query causes a panic.")
        else:
            print("No suitable property found for searching")
            print("Try modifying this script to search for a specific property value")
    else:
        print("No sample record found")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()


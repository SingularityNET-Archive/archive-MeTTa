#!/usr/bin/env python3
"""
Example 1: List Atom Types

This script demonstrates the hybrid approach:
- Uses SQL to get database schema (tables and columns)
- Lists atom types without loading all data into MeTTa
- Optionally loads a minimal sample for verification
"""

from connect import list_atom_types, get_tables, get_columns

def main():
    print("=" * 60)
    print("Example 1: List Atom Types")
    print("=" * 60)
    print("Using hybrid approach: SQL schema → Atom types\n")
    
    # Step 1: Get atom types directly from database schema (fast, no MeTTa needed)
    print("Step 1: Getting atom types from database schema...")
    print("  Querying: information_schema.tables and information_schema.columns")
    
    # Get types from schema (no MeTTa loading required)
    types = list_atom_types(None, verify_existence=False)
    
    print(f"  ✓ Found {len(types['entity_types'])} entity types\n")
    
    # Display the types
    print("=" * 60)
    print("ATOM TYPES IN DATABASE SCHEMA")
    print("=" * 60)
    print()
    
    for entity_type in types['entity_types']:
        print(f"  • :{entity_type}")
        props = types['property_types'].get(entity_type, [])
        if props:
            # Show first 10 properties
            prop_list = ', '.join([f":{entity_type}.{p}" for p in props[:10]])
            print(f"    Properties: {prop_list}")
            if len(props) > 10:
                print(f"    ... and {len(props) - 10} more properties")
        print()
    
    print("=" * 60)
    print("Why this approach?")
    print("=" * 60)
    print("""
✅ No need to load 100k+ atoms just to see types
✅ Fast - queries database schema directly
✅ Accurate - types come from actual database structure
✅ No panics - doesn't touch MeTTa space at all
✅ Can run before loading any data

Note: Atom types are determined by your database schema:
  - Tables → Entity types (:table_name)
  - Columns → Properties (:table_name.column_name)

These types will be available once you load data into MeTTa.
    """)
    
    print("=" * 60)
    print("Done!")
    print("=" * 60)
    print("\nTip: To verify types exist in MeTTa space, load data first:")
    print("     from hyperon import MeTTa")
    print("     from connect import load_all, print_atom_types")
    print("     interp = MeTTa()")
    print("     load_all(interp)")
    print("     print_atom_types(interp, verify_existence=False)")

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Example 5: Hybrid SQL + MeTTa Approach (Recommended for Production)

This demonstrates the recommended pattern:
1. Use SQL to filter/limit large datasets
2. Pass filtered IDs to MeTTa for reasoning/pattern matching

This is the best approach for production use.
"""

from hyperon import MeTTa
from connect import load_all, query_batch, cursor

def main():
    print("=" * 60)
    print("Example 5: Hybrid SQL + MeTTa Approach")
    print("=" * 60)
    print("Recommended pattern for production use\n")
    
    # Initialize MeTTa interpreter
    interp = MeTTa()
    
    # Load data
    print("Loading data into MeTTa...")
    load_all(interp)
    print("Data loaded!\n")
    
    # Step 1: Use SQL to filter/limit (fast, handles large datasets)
    print("Step 1: Using SQL to filter records...")
    print("  Query: SELECT id FROM action_items WHERE status = 'active' LIMIT 10")
    
    try:
        cursor.execute("""
            SELECT id FROM action_items 
            WHERE status = 'active'
            LIMIT 10
        """)
        filtered_ids = [row[0] for row in cursor.fetchall()]
        print(f"  ✓ Found {len(filtered_ids)} records using SQL\n")
        
        if filtered_ids:
            # Step 2: Use MeTTa for reasoning on filtered set (small, safe)
            print("Step 2: Querying MeTTa for filtered IDs...")
            print(f"  Querying {len(filtered_ids)} records from MeTTa...")
            
            results = query_batch(
                interp,
                "action_items",
                filtered_ids,
                ["text", "assignee", "status"],
                batch_size=50
            )
            
            print(f"  ✓ Retrieved {len(results)} records from MeTTa\n")
            
            # Step 3: Process results (could do reasoning, pattern matching, etc.)
            print("Step 3: Processing results...")
            for i, result in enumerate(results, 1):
                text = result.get('text', 'N/A')
                if len(text) > 50:
                    text = text[:47] + "..."
                print(f"  {i}. [{result.get('status', 'N/A')}] {result.get('assignee', 'N/A')}: {text}")
        else:
            print("  No records found matching criteria")
            
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("Why This Approach?")
    print("=" * 60)
    print("""
✅ SQL is fast at filtering large datasets
✅ Avoids MeTTa panics by limiting result sets  
✅ Best performance - use the right tool for each job
✅ Scalable - works with millions of records
✅ Flexible - SQL for filtering, MeTTa for reasoning

Use SQL for:
  - Filtering, WHERE clauses
  - Joins between tables
  - Aggregations (COUNT, SUM, etc.)
  - Date ranges, text search
  - Large scans

Use MeTTa for:
  - Pattern matching on filtered results
  - Reasoning and inference
  - Knowledge graph queries
  - Small result sets
    """)
    
    print("=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()


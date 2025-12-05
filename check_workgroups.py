#!/usr/bin/env python3
"""
Diagnostic script to check workgroups table in Supabase.
This will help identify why only 1 workgroup is showing in the Supabase table editor.
"""

from connect import cursor, get_tables, fetch_table

def main():
    print("=" * 60)
    print("Workgroups Table Diagnostic")
    print("=" * 60)
    
    # Get all tables
    tables = get_tables()
    print(f"\nFound {len(tables)} tables in database:")
    for table in tables:
        print(f"  - {table}")
    
    # Look for workgroup-related tables
    workgroup_tables = [t for t in tables if 'workgroup' in t.lower()]
    
    if not workgroup_tables:
        print("\n⚠️  No table with 'workgroup' in the name found.")
        print("   Checking all tables for workgroup-related data...")
        
        # Check each table for workgroup columns
        for table in tables:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                  AND table_name = %s
                  AND column_name ILIKE '%workgroup%'
            """, (table,))
            cols = cursor.fetchall()
            if cols:
                print(f"\n  Found workgroup columns in '{table}':")
                for col in cols:
                    print(f"    - {col[0]}")
    else:
        print(f"\n✓ Found {len(workgroup_tables)} workgroup table(s):")
        for table in workgroup_tables:
            print(f"  - {table}")
    
    # Check each workgroup table
    for table in workgroup_tables:
        print(f"\n{'=' * 60}")
        print(f"Analyzing table: {table}")
        print(f"{'=' * 60}")
        
        # Count total rows
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        total_count = cursor.fetchone()[0]
        print(f"\nTotal rows in database: {total_count}")
        
        # Check for RLS policies
        cursor.execute("""
            SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
            FROM pg_policies 
            WHERE tablename = %s
        """, (table,))
        policies = cursor.fetchall()
        
        if policies:
            print(f"\n⚠️  Row Level Security (RLS) policies found: {len(policies)}")
            print("   These policies may filter what you see in Supabase UI:")
            for policy in policies:
                print(f"     - Policy: {policy[2]}")
                print(f"       Command: {policy[5]}")
                print(f"       Roles: {policy[4]}")
                if policy[6]:
                    print(f"       Condition: {policy[6]}")
        else:
            print("\n✓ No RLS policies found (all rows should be visible)")
        
        # Check if RLS is enabled
        cursor.execute("""
            SELECT tablename, rowsecurity 
            FROM pg_tables 
            WHERE schemaname = 'public' 
              AND tablename = %s
        """, (table,))
        rls_info = cursor.fetchall()
        if rls_info:
            rls_enabled = rls_info[0][1]
            if rls_enabled:
                print("\n⚠️  RLS (Row Level Security) is ENABLED on this table")
                print("   This means policies may be filtering results in Supabase UI")
            else:
                print("\n✓ RLS is disabled (all rows should be visible)")
        
        # Fetch all rows to see what we get
        print(f"\nFetching all rows from {table}...")
        try:
            rows = fetch_table(table)
            print(f"✓ Retrieved {len(rows)} rows via Python connection")
            
            if len(rows) != total_count:
                print(f"\n⚠️  MISMATCH: Database has {total_count} rows, but fetch_table() got {len(rows)}")
                print("   This suggests filtering is happening somewhere.")
            else:
                print(f"✓ Row count matches: {len(rows)} rows")
            
            # Show first few rows
            if rows:
                print(f"\nFirst {min(5, len(rows))} rows:")
                for i, row in enumerate(rows[:5], 1):
                    print(f"  {i}. {row}")
            
        except Exception as e:
            print(f"✗ Error fetching rows: {e}")
        
        # Check for views that might be filtering
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public'
              AND table_name ILIKE '%workgroup%'
        """)
        views = cursor.fetchall()
        if views:
            print(f"\n⚠️  Found {len(views)} view(s) with 'workgroup' in name:")
            for view in views:
                print(f"     - {view[0]}")
            print("   Make sure you're looking at the TABLE, not a VIEW in Supabase UI")
    
    print("\n" + "=" * 60)
    print("Common reasons for missing rows in Supabase UI:")
    print("=" * 60)
    print("""
1. Row Level Security (RLS) policies filtering results
   → Check the policies shown above
   → Disable RLS or adjust policies if needed

2. Pagination in Supabase UI
   → Check if there's a "Load more" or pagination control
   → Supabase UI may show limited rows per page

3. Default filters in Supabase UI
   → Check for any filter icons or WHERE clauses in the UI
   → Clear all filters

4. Viewing a VIEW instead of a TABLE
   → Make sure you're in the "Tables" section, not "Views"

5. Connection/user permissions
   → The user account may have limited permissions
   → Check if you're using the correct database role
    """)

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Script to find and list documenters from the database using SQL.
"""

from connect import cursor, get_tables, get_columns

def find_documenter_tables():
    """Find tables and columns related to documenters."""
    tables = get_tables()
    documenter_info = []
    
    print("Searching for documenter-related tables and columns...\n")
    
    for table in tables:
        # Check if table name contains documenter
        if 'documenter' in table.lower():
            documenter_info.append({
                'table': table,
                'type': 'table_name',
                'columns': [col[0] for col in get_columns(table)]
            })
        
        # Check columns for documenter references
        columns = get_columns(table)
        documenter_cols = [col[0] for col in columns if 'documenter' in col[0].lower()]
        
        if documenter_cols:
            documenter_info.append({
                'table': table,
                'type': 'column',
                'columns': documenter_cols
            })
    
    return documenter_info

def generate_sql_queries(documenter_info):
    """Generate SQL queries based on discovered documenter data."""
    queries = []
    
    if not documenter_info:
        print("⚠️  No documenter tables or columns found.")
        print("\nCommon SQL patterns to list documenters:")
        print("=" * 60)
        print("""
-- If there's a documenters table:
SELECT * FROM documenters;

-- If documenter is a column in another table:
SELECT DISTINCT documenter FROM meetings;
SELECT DISTINCT documenter_id FROM meetings;

-- If documenters are in a users table with a role:
SELECT * FROM users WHERE role = 'documenter';

-- If documenters are linked via a junction table:
SELECT d.* 
FROM documenters d
JOIN workgroup_documenters wd ON d.id = wd.documenter_id
WHERE wd.workgroup_id = 1;

-- Count documenters:
SELECT COUNT(*) FROM documenters;
SELECT COUNT(DISTINCT documenter) FROM meetings;
        """)
        return
    
    print("=" * 60)
    print("Found documenter-related data:")
    print("=" * 60)
    
    for info in documenter_info:
        table = info['table']
        cols = info['columns']
        
        if info['type'] == 'table_name':
            print(f"\n✓ Table: {table}")
            print(f"  Columns: {', '.join(cols)}")
            
            queries.append({
                'description': f'List all documenters from {table}',
                'sql': f'SELECT * FROM {table};'
            })
            
            queries.append({
                'description': f'Count documenters in {table}',
                'sql': f'SELECT COUNT(*) as total_documenters FROM {table};'
            })
            
            # If there's an id column, we can list with IDs
            if 'id' in cols:
                queries.append({
                    'description': f'List documenters with IDs from {table}',
                    'sql': f'SELECT id, * FROM {table} ORDER BY id;'
                })
        
        elif info['type'] == 'column':
            print(f"\n✓ Table: {table}")
            print(f"  Documenter columns: {', '.join(cols)}")
            
            for col in cols:
                queries.append({
                    'description': f'List unique documenters from {table}.{col}',
                    'sql': f'SELECT DISTINCT {col} FROM {table} WHERE {col} IS NOT NULL ORDER BY {col};'
                })
                
                queries.append({
                    'description': f'Count unique documenters in {table}.{col}',
                    'sql': f'SELECT COUNT(DISTINCT {col}) as total_documenters FROM {table} WHERE {col} IS NOT NULL;'
                })
                
                queries.append({
                    'description': f'List all rows with documenter info from {table}',
                    'sql': f'SELECT * FROM {table} WHERE {col} IS NOT NULL ORDER BY {col};'
                })
    
    return queries

def main():
    print("=" * 60)
    print("Documenter SQL Query Generator")
    print("=" * 60)
    print()
    
    # Find documenter-related data
    documenter_info = find_documenter_tables()
    
    # Generate SQL queries
    queries = generate_sql_queries(documenter_info)
    
    if queries:
        print("\n" + "=" * 60)
        print("Generated SQL Queries:")
        print("=" * 60)
        
        for i, query_info in enumerate(queries, 1):
            print(f"\n{i}. {query_info['description']}")
            print(f"   {query_info['sql']}")
        
        print("\n" + "=" * 60)
        print("Quick Copy-Paste Queries:")
        print("=" * 60)
        
        # Show the most useful queries
        if documenter_info:
            first_info = documenter_info[0]
            table = first_info['table']
            
            if first_info['type'] == 'table_name':
                print(f"\n-- List all documenters:")
                print(f"SELECT * FROM {table};")
                
                print(f"\n-- List documenters with specific columns:")
                cols_str = ', '.join(first_info['columns'][:5])  # First 5 columns
                print(f"SELECT {cols_str} FROM {table};")
            else:
                col = first_info['columns'][0]
                print(f"\n-- List unique documenters:")
                print(f"SELECT DISTINCT {col} FROM {table} WHERE {col} IS NOT NULL ORDER BY {col};")
                
                print(f"\n-- List all records with documenter info:")
                print(f"SELECT * FROM {table} WHERE {col} IS NOT NULL ORDER BY {col};")
    
    print("\n" + "=" * 60)
    print("Tips:")
    print("=" * 60)
    print("""
• Run these queries in Supabase SQL Editor or your database client
• Use DISTINCT to get unique documenter names/IDs
• Add WHERE clauses to filter by workgroup, date, etc.
• Use JOINs if documenters are linked across multiple tables
• Add ORDER BY to sort results alphabetically or by date
    """)

if __name__ == "__main__":
    main()


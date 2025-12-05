#!/usr/bin/env python3
import os
import psycopg2
from urllib.parse import urlparse
from pprint import pprint
from dotenv import load_dotenv

from hyperon import MeTTa

# -------------------------------------------------------------
# ENV + CONFIG
# -------------------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DB_PASSWORD  = os.getenv("DB_PASSWORD")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL missing")
if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD missing")

# -------------------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------------------
url = urlparse(DATABASE_URL)

conn = psycopg2.connect(
    dbname=url.path[1:],
    user=url.username,
    password=DB_PASSWORD,
    host=url.hostname,
    port=url.port
)

cursor = conn.cursor()


# -------------------------------------------------------------
# SCHEMA FUNCTIONS
# -------------------------------------------------------------
def get_tables():
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    return [row[0] for row in cursor.fetchall()]


def get_columns(table):
    cursor.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema='public'
          AND table_name=%s
        ORDER BY ordinal_position;
    """, (table,))
    return cursor.fetchall()


def get_foreign_keys(table):
    cursor.execute("""
    SELECT
        kcu.column_name,
        ccu.table_name AS foreign_table,
        ccu.column_name AS foreign_column
    FROM 
        information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
      AND tc.table_name = %s;
    """, (table,))
    return cursor.fetchall()


def get_full_schema():
    schema = {}
    for t in get_tables():
        schema[t] = {
            "columns": get_columns(t),
            "foreign_keys": get_foreign_keys(t)
        }
    return schema


# -------------------------------------------------------------
# DATA FETCH
# -------------------------------------------------------------
def fetch_table(table):
    cursor.execute(f"SELECT * FROM {table}")
    if cursor.description is None:
        return []
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


# -------------------------------------------------------------
# SAFE VALUE ENCODING
# -------------------------------------------------------------
def extract_query_value(result):
    """
    Extract the actual value from a MeTTa query result.
    MeTTa returns results as nested lists: [[value]] or [[$var]]
    Returns the first value found, or None if empty.
    """
    if not result or not isinstance(result, list) or len(result) == 0:
        return None
    first_match = result[0]
    if isinstance(first_match, list) and len(first_match) > 0:
        return first_match[0]
    return first_match


def encode_value(val):
    """
    Safely encode Python values as MeTTa literals:
    - int/float -> raw number
    - bool -> True/False
    - None -> Null
    - str -> safely escaped string
    """
    if val is None:
        return "Null"
    elif isinstance(val, bool):
        return "True" if val else "False"
    elif isinstance(val, (int, float)):
        return str(val)
    else:
        s = str(val)
        # Escape backslashes first
        s = s.replace("\\", "\\\\")
        # Escape quotes
        s = s.replace('"', '\\"')
        # Normalize control characters
        s = s.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        # Replace any other non-printable characters
        s = "".join(ch if 32 <= ord(ch) <= 126 else " " for ch in s)
        return f'"{s}"'


def row_to_atoms(table, row):
    """
    Convert a database row into structured MeTTa atoms.
    Example:
      row = {"id": 1, "title": "Meeting"}
      atoms -> 
        (:table 1)
        (:table.title 1 "Meeting")
    """
    atoms = []
    rid = row.get("id")

    if rid is not None:
        atoms.append(f"(:{table} {encode_value(rid)})")

    for col, val in row.items():
        if col != "id":
            atoms.append(f"(:{table}.{col} {encode_value(rid)} {encode_value(val)})")

    return atoms


# -------------------------------------------------------------
# ATOM TYPE DISCOVERY
# -------------------------------------------------------------
def list_atom_types(interp, verify_existence=True):
    """
    List all atom types that have been mapped from database fields.
    
    Returns a dict with:
    - 'entity_types': List of table names (e.g., ['action_items', 'meetings'])
    - 'property_types': Dict mapping table -> list of property names
    - 'verified': Whether types were verified to exist in MeTTa space
    
    Args:
        interp: MeTTa interpreter
        verify_existence: If True, verify each type exists by querying a sample atom
    """
    tables = get_tables()
    entity_types = []
    property_types = {}
    
    for table in tables:
        entity_types.append(table)
        columns = get_columns(table)
        property_names = [col[0] for col in columns if col[0] != 'id']
        property_types[table] = property_names
    
    result = {
        'entity_types': entity_types,
        'property_types': property_types,
        'verified': False
    }
    
    # Optionally verify types exist in MeTTa by checking a sample atom
    if verify_existence:
        verified_entity_types = []
        verified_property_types = {}
        
        for table in entity_types:
            # Check if at least one entity of this type exists
            sample_rows = fetch_table(table)[:1]
            if sample_rows and sample_rows[0].get("id"):
                sample_id = sample_rows[0]["id"]
                encoded_id = encode_value(sample_id)
                try:
                    query = f'!(match &self (:{table} {encoded_id}) $result)'
                    results = interp.run(query)
                    if results and len(results) > 0:
                        verified_entity_types.append(table)
                        
                        # Verify properties for this entity
                        verified_props = []
                        for prop in property_types[table][:5]:  # Check first 5 props only
                            try:
                                prop_query = f'!(match &self (:{table}.{prop} {encoded_id} $val) $val)'
                                prop_results = interp.run(prop_query)
                                if prop_results and len(prop_results) > 0:
                                    verified_props.append(prop)
                            except Exception:
                                pass  # Skip properties that cause errors
                        
                        if verified_props:
                            verified_property_types[table] = verified_props
                except Exception:
                    pass  # Skip tables that cause errors
        
        result['verified_entity_types'] = verified_entity_types
        result['verified_property_types'] = verified_property_types
        result['verified'] = True
    
    return result


def print_atom_types(interp, verify_existence=True):
    """
    Print a human-readable list of atom types.
    """
    types = list_atom_types(interp, verify_existence)
    
    print("\n=== ATOM TYPES IN METTA SPACE ===\n")
    
    if types['verified']:
        print("Entity Types (verified in space):")
        for entity_type in types.get('verified_entity_types', []):
            print(f"  • :{entity_type}")
            props = types.get('verified_property_types', {}).get(entity_type, [])
            if props:
                print(f"    Properties: {', '.join([f':{entity_type}.{p}' for p in props[:10]])}")
                if len(props) > 10:
                    print(f"    ... and {len(props) - 10} more properties")
        print()
        print("Note: Only verified types are shown (types with at least one atom in space)")
    else:
        print("Entity Types (from database schema):")
        for entity_type in types['entity_types']:
            print(f"  • :{entity_type}")
            props = types['property_types'].get(entity_type, [])
            if props:
                print(f"    Properties: {', '.join([f':{entity_type}.{p}' for p in props[:10]])}")
                if len(props) > 10:
                    print(f"    ... and {len(props) - 10} more properties")
        print()
        print("Note: Types listed from schema. Use verify_existence=True to check MeTTa space.")


# -------------------------------------------------------------
# PRODUCTION QUERY HELPERS
# -------------------------------------------------------------
def query_by_id(interp, table, record_id, properties=None):
    """
    Production-safe: Query a specific record by ID.
    
    Args:
        interp: MeTTa interpreter
        table: Table name
        record_id: Record ID to query
        properties: Optional list of property names to extract
    
    Returns:
        dict with 'id' and requested properties
    """
    encoded_id = encode_value(record_id)
    result = {"id": record_id}
    
    # Check if record exists
    try:
        query = f'!(match &self (:{table} {encoded_id}) $result)'
        exists = interp.run(query)
        if not exists or len(exists) == 0:
            return None
    except Exception:
        return None
    
    # Extract properties if requested
    if properties:
        for prop in properties:
            try:
                query = f'!(match &self (:{table}.{prop} {encoded_id} $val) $val)'
                prop_results = interp.run(query)
                if prop_results and len(prop_results) > 0:
                    result[prop] = extract_query_value(prop_results)
            except KeyboardInterrupt:
                # User interrupted, stop processing
                break
            except Exception:
                # Property query failed (may cause panic with some properties)
                # Set to None and continue with other properties
                result[prop] = None
    
    return result


def query_batch(interp, table, record_ids, properties=None, batch_size=50):
    """
    Production-safe: Query multiple records in batches.
    
    Args:
        interp: MeTTa interpreter
        table: Table name
        record_ids: List of record IDs
        properties: Optional list of property names
        batch_size: Number of records per batch (default 50)
    
    Returns:
        List of result dicts
    """
    results = []
    for i in range(0, len(record_ids), batch_size):
        batch = record_ids[i:i + batch_size]
        for record_id in batch:
            result = query_by_id(interp, table, record_id, properties)
            if result:
                results.append(result)
    return results


def query_by_property_value(interp, table, property_name, value):
    """
    Production-safe: Find IDs by property value (use for small result sets).
    
    WARNING: Only use when you expect <1000 results, otherwise use SQL.
    
    Args:
        interp: MeTTa interpreter
        table: Table name
        property_name: Property to search
        value: Value to match
    
    Returns:
        List of matching record IDs
    """
    encoded_value = encode_value(value)
    try:
        # Query: find all records where property = value
        query = f'!(match &self (:{table}.{property_name} $id {encoded_value}) $id)'
        results = interp.run(query)
        
        if not results:
            return []
        
        # Extract IDs from results
        ids = []
        for result in results:
            if isinstance(result, list) and len(result) > 0:
                id_val = extract_query_value([result])
                if id_val:
                    ids.append(id_val)
        
        return ids
    except Exception as e:
        print(f"Query failed: {e}")
        return []


# -------------------------------------------------------------
# LOAD DATA INTO METTA
# -------------------------------------------------------------
def load_all(interp):
    tables = get_tables()
    total_atoms = 0

    for t in tables:
        rows = fetch_table(t)
        print(f"Loading table: {t} ({len(rows)} rows)")

        for row in rows:
            atoms = row_to_atoms(t, row)
            for atom_str in atoms:
                # Insert directly into MeTTa space
                interp.run(f"!(add-atom &self {atom_str})")
                total_atoms += 1

    print(f"\n✓ Loaded {total_atoms} atoms into MeTTa\n")


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
if __name__ == "__main__":

    print("\n=== DATABASE SCHEMA ===")
    pprint(get_full_schema())

    print("\n=== SAMPLE DATA ===")
    for t in get_tables():
        print(f"\nTable: {t}")
        pprint(fetch_table(t)[:5])  # show only first 5 rows for brevity

    print("\n=== LOADING INTO METTA ===")
    interp = MeTTa()
    load_all(interp)

    print("\n=== ATOM TYPES ===")
    print_atom_types(interp, verify_existence=True)

    print("=== BASIC QUERY EXAMPLES ===")

    tables = get_tables()
    if tables:
        first = tables[0]
        
        # Get a sample ID from the database to test with a specific query
        sample_rows = fetch_table(first)[:1]
        if sample_rows and sample_rows[0].get("id"):
            sample_id = sample_rows[0]["id"]
            encoded_id = encode_value(sample_id)
            
            # Query 1: Test exact match (confirms atom exists)
            print(f"\nQuery 1: Testing exact match for ID from '{first}'")
            try:
                query = f'!(match &self (:{first} {encoded_id}) $result)'
                print(f"  {query}")
                results = interp.run(query)
                print(f"  Results: {results}")
                print(f"  Interpretation: {results} means:")
                print(f"    - Found {len(results)} match(es)")
                print(f"    - Each match is: {results[0] if results else 'N/A'}")
                print(f"    - The $result variable wasn't bound (no variables in pattern)")
                if results and isinstance(results, list) and len(results) > 0:
                    print(f"  ✓ Atom exists in space!")
            except Exception as e:
                print(f"  ✗ Error: {e}")
            
            # Query 2: Extract multiple property values (shows actual data extraction)
            print(f"\nQuery 2: Extracting property values for ID: {sample_id}")
            # Get property column names (skip 'id', limit to first 3 to avoid panics)
            # Note: Some property queries may cause Rust panics that can't be caught
            cols = [c[0] for c in get_columns(first) if c[0] != 'id'][:3]
            if cols:
                print(f"  Querying {len(cols)} properties: {', '.join(cols)}")
                print()
                extracted_data = {}
                skipped = []
                
                for prop_name in cols:
                    try:
                        # Query for the property value: (:table.property id $val)
                        query = f'!(match &self (:{first}.{prop_name} {encoded_id} $val) $val)'
                        results = interp.run(query)
                        if results and isinstance(results, list) and len(results) > 0:
                            actual_value = extract_query_value(results)
                            if actual_value:
                                extracted_data[prop_name] = actual_value
                                # Display value (truncate if too long)
                                display_value = str(actual_value)
                                if len(display_value) > 60:
                                    display_value = display_value[:57] + "..."
                                print(f"  {prop_name:20s} = {display_value}")
                            else:
                                print(f"  {prop_name:20s} = <no value>")
                        else:
                            print(f"  {prop_name:20s} = <not found>")
                    except KeyboardInterrupt:
                        print(f"\n  Interrupted by user")
                        break
                    except Exception as e:
                        error_msg = str(e)[:40]
                        print(f"  {prop_name:20s} = <error: {error_msg}...>")
                        skipped.append(prop_name)
                    except:
                        # Catch Rust panics that might not be caught by Exception
                        print(f"  {prop_name:20s} = <panic occurred>")
                        skipped.append(prop_name)
                        # Note: Rust panics may crash the process, so we may not reach here
                
                print()
                if extracted_data:
                    print(f"  ✓ Successfully extracted {len(extracted_data)} property values")
                if skipped:
                    print(f"  ⚠ Skipped {len(skipped)} properties due to errors: {', '.join(skipped)}")
                if not extracted_data and not skipped:
                    print(f"  ✗ No values extracted")
        
        # Note about variable queries
        print(f"\nNote: Variable queries like '!(match &self (:{first} $id) $id)'")
        print(f"      may cause panics with large result sets (>10k matches).")
        print(f"      Use specific ID queries or filter queries for production use.")

    print("\n=== PRODUCTION SCALING PATTERNS ===\n")
    
    # Demonstrate production query functions
    tables = get_tables()
    if tables:
        first = tables[0]
        sample_rows = fetch_table(first)[:1]
        
        if sample_rows and sample_rows[0].get("id"):
            sample_id = sample_rows[0]["id"]
            
            print("Example 1: Query by specific ID (production-safe)")
            result = query_by_id(interp, first, sample_id, ["text", "assignee"])
            if result:
                print(f"  Found record: {result.get('id')}")
                for key, val in result.items():
                    if key != 'id':
                        display = str(val)[:50] + "..." if len(str(val)) > 50 else str(val)
                        print(f"    {key}: {display}")
            
            print("\nExample 2: Hybrid approach (SQL + MeTTa)")
            print("  Step 1: Use SQL to filter/limit results")
            print(f"    SELECT id FROM {first} LIMIT 5")
            limited_ids = [row["id"] for row in fetch_table(first)[:5]]
            print(f"  Step 2: Query MeTTa for filtered IDs only")
            print(f"    Processing {len(limited_ids)} IDs...")
            batch_results = query_batch(interp, first, limited_ids[:3], ["text"], batch_size=10)
            print(f"  ✓ Retrieved {len(batch_results)} records from MeTTa")
    
    print("""
Production Best Practices:

1. SPECIFIC ID QUERIES (Safe - Recommended)
   ✓ Use: query_by_id(interp, table, id, properties)
   ✓ Use when: You know the specific ID(s) you need
   ✓ Performance: Fast, no panics

2. DATABASE-FIRST APPROACH (Best for large queries)
   ✓ Use SQL for: Filtering, joins, aggregations, large scans
   ✓ Then query MeTTa only for the filtered IDs
   ✓ Use when: You need to filter/aggregate large datasets

3. BATCH PROCESSING (For multiple IDs)
   ✓ Use: query_batch(interp, table, ids, properties, batch_size=50)
   ✓ Process IDs in small batches (10-100 at a time)
   ✓ Use when: You have a list of IDs to process

4. HYBRID APPROACH (Recommended)
   ✓ Use SQL for: Filtering, joins, aggregations, large scans
   ✓ Use MeTTa for: Pattern matching, reasoning, small result sets
   ✓ Use when: You need both SQL power and MeTTa reasoning

5. AVOID (Causes panics):
   ✗ Variable queries returning >10k results
   ✗ get_atoms() or atom_count() with large spaces
   ✗ Querying all atoms of a type without filters
   ✗ query_by_property_value() with >1000 expected results
    """)

    print("\n=== READY ===\n")

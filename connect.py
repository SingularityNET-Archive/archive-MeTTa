from supabase import create_client

# Replace with your own Supabase credentials

# Note: You'll need to set SUPABASE_URL and SUPABASE_KEY
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_table(table_name):
    response = supabase.table(table_name).select("*").execute()
    return response.data

-- ============================================================
-- SQL Queries to List Documenters
-- ============================================================
-- Run these in Supabase SQL Editor or your database client
-- ============================================================

-- ============================================================
-- Basic Queries
-- ============================================================

-- 1. List all documenters (if documenters table exists)
SELECT * FROM documenters;

-- 2. List documenters with specific columns
SELECT id, name, email, created_at 
FROM documenters 
ORDER BY name;

-- 3. Count total documenters
SELECT COUNT(*) as total_documenters 
FROM documenters;

-- ============================================================
-- If documenter is a column in another table
-- ============================================================

-- 4. List unique documenter names/IDs
SELECT DISTINCT documenter 
FROM meetings 
WHERE documenter IS NOT NULL 
ORDER BY documenter;

-- 5. Count unique documenters
SELECT COUNT(DISTINCT documenter) as total_documenters 
FROM meetings 
WHERE documenter IS NOT NULL;

-- 6. List all meetings/records with documenter info
SELECT * 
FROM meetings 
WHERE documenter IS NOT NULL 
ORDER BY documenter, date DESC;

-- ============================================================
-- If documenters are linked via foreign keys
-- ============================================================

-- 7. List documenters with their workgroups
SELECT 
    d.id,
    d.name,
    d.email,
    wg.name as workgroup_name
FROM documenters d
JOIN workgroup_documenters wd ON d.id = wd.documenter_id
JOIN workgroups wg ON wd.workgroup_id = wg.id
ORDER BY wg.name, d.name;

-- 8. List documenters for a specific workgroup
SELECT d.*
FROM documenters d
JOIN workgroup_documenters wd ON d.id = wd.documenter_id
WHERE wd.workgroup_id = 1;  -- Replace 1 with your workgroup ID

-- ============================================================
-- If documenters are users with a role
-- ============================================================

-- 9. List users who are documenters
SELECT * 
FROM users 
WHERE role = 'documenter' 
   OR role = 'Documenter'
ORDER BY name;

-- 10. List documenters with their activity count
SELECT 
    documenter,
    COUNT(*) as meeting_count,
    MIN(date) as first_meeting,
    MAX(date) as last_meeting
FROM meetings
WHERE documenter IS NOT NULL
GROUP BY documenter
ORDER BY meeting_count DESC;

-- ============================================================
-- Advanced Queries
-- ============================================================

-- 11. List documenters with their associated workgroups count
SELECT 
    d.id,
    d.name,
    COUNT(DISTINCT wd.workgroup_id) as workgroup_count
FROM documenters d
LEFT JOIN workgroup_documenters wd ON d.id = wd.documenter_id
GROUP BY d.id, d.name
ORDER BY workgroup_count DESC, d.name;

-- 12. Find documenters who haven't been assigned to any workgroup
SELECT d.*
FROM documenters d
LEFT JOIN workgroup_documenters wd ON d.id = wd.documenter_id
WHERE wd.documenter_id IS NULL;

-- 13. List documenters with their recent meetings
SELECT 
    d.name as documenter,
    m.title as meeting_title,
    m.date,
    wg.name as workgroup
FROM documenters d
JOIN meetings m ON m.documenter_id = d.id
JOIN workgroups wg ON m.workgroup_id = wg.id
WHERE m.date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY m.date DESC, d.name;

-- ============================================================
-- Search/Filter Queries
-- ============================================================

-- 14. Search documenters by name
SELECT * 
FROM documenters 
WHERE name ILIKE '%john%'  -- Replace 'john' with search term
ORDER BY name;

-- 15. List documenters created in the last month
SELECT * 
FROM documenters 
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY created_at DESC;

-- ============================================================
-- Notes:
-- ============================================================
-- • Adjust table/column names based on your actual schema
-- • Replace placeholder IDs (like workgroup_id = 1) with actual values
-- • Use ILIKE for case-insensitive text search in PostgreSQL
-- • Add LIMIT clauses if you have many results:
--   SELECT * FROM documenters LIMIT 100;
-- ============================================================


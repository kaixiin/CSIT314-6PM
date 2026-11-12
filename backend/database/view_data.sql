-- Shows the data in every table, for checking and for report screenshots.
-- Run after schema.sql, seed.sql and the two generator scripts (see README.md).
-- Run one query at a time: put the cursor on it and press Ctrl+Enter.
-- In Workbench, set the "Limit to ... rows" dropdown in the toolbar to "Don't Limit",
-- or idp_view (about 1,600 rows) is cut off at 1000.
-- Rows are in insert order, so the generated data is at the bottom of each result.

USE interior_design_platform;

-- 1. user_profile: the 4 roles from seed.sql
SELECT * FROM user_profile
ORDER BY profile_id;

-- 2. user_account: 4 seed accounts, then 180 generated ones (@test123.com).
--    password is left out so it does not show in screenshots.
SELECT account_id, profile_id, username, email, is_suspended
FROM user_account
ORDER BY account_id;

-- 3. company_profile: 1 seed company, then 100 generated ones
SELECT * FROM company_profile
ORDER BY company_id;

-- 4. idp_category: 10 seed categories, then 90 generated ones
SELECT * FROM idp_category
ORDER BY category_id;

-- 5. idp: 100 generated projects
SELECT * FROM idp
ORDER BY idp_id;

-- 6. favourite: about 200 generated favourites
SELECT * FROM favourite
ORDER BY favourite_id;

-- 7. idp_view: about 1,600 generated views
SELECT * FROM idp_view
ORDER BY view_id;

-- 8. Row count of every table
SELECT 'user_profile' AS table_name, COUNT(*) AS total_rows FROM user_profile
UNION ALL SELECT 'user_account', COUNT(*) FROM user_account
UNION ALL SELECT 'company_profile', COUNT(*) FROM company_profile
UNION ALL SELECT 'idp_category', COUNT(*) FROM idp_category
UNION ALL SELECT 'idp', COUNT(*) FROM idp
UNION ALL SELECT 'favourite', COUNT(*) FROM favourite
UNION ALL SELECT 'idp_view', COUNT(*) FROM idp_view;

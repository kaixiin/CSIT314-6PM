USE interior_design_platform;

INSERT INTO user_profile (name, account_type, description) VALUES 
('User Admin', 'UserAdmin', 'Manages system users, accounts, and application permissions.'), 
('Interior Designer', 'InteriorDesigner', 'Creates spatial mockups, manages design boards, and collaborates with clients.'),
('Customer', 'Customer', 'Browses interior portfolios, requests design quotes, and reviews project timelines.'),
('Platform Manager', 'PlatformManager', 'Oversees overall site activity, application metrics, and global system health.');

INSERT INTO user_account (profile_id, username, password, email) VALUES
(1, 'admin01', 'admin123', 'admin01@test.com'),
(2, 'id01', 'id123', 'id01@test.com'),
(3, 'cust01', 'cust123', 'cust01@test.com'),
(4, 'pm01', 'pm123', 'pm01@test.com');

INSERT INTO company_profile (account_id, company_name, description, address, contact_number, email) VALUES
(2, 'Test Design Studio', 'Test interior design company', '10 Orchard Road, Singapore', '61234567', 'hello@test.com');

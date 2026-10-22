USE interior_design_platform;

INSERT INTO user_profile (name, account_type) VALUES 
('User Admin','UserAdmin'), 
('Interior Designer','InteriorDesigner'),
('Customer', 'Customer'),
('Platform Manager', 'PlatformManager');

INSERT INTO user_account (profile_id, username, password, email) VALUES
(1, 'admin01', 'admin123', 'admin01@test.com'),
(2, 'id01', 'id123', 'id01@test.com'),
(3, 'cust01', 'cust123', 'cust01@test.com'),
(4, 'pm01', 'pm123', 'pm01@test.com');



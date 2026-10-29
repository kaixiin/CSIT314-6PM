CREATE DATABASE IF NOT EXISTS interior_design_platform
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE interior_design_platform;

CREATE TABLE user_profile (
  profile_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL UNIQUE,
  account_type VARCHAR(50) NOT NULL UNIQUE,
  is_suspended BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(profile_id)
);

CREATE TABLE user_account (
  account_id INT NOT NULL AUTO_INCREMENT,
  profile_id INT NOT NULL,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  is_suspended BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(account_id),
  FOREIGN KEY (profile_id) REFERENCES user_profile(profile_id)
);

CREATE TABLE company_profile (
  company_id INT NOT NULL AUTO_INCREMENT,
  account_id INT NOT NULL UNIQUE,
  company_name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  address VARCHAR(255),
  contact_number VARCHAR(20),
  email VARCHAR(255),
  logo VARCHAR(255),
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(company_id),
  FOREIGN KEY(account_id) REFERENCES user_account(account_id)
);
CREATE DATABASE IF NOT EXISTS interior_design_platform
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE interior_design_platform;

CREATE TABLE user_profile (
  profile_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL UNIQUE,
  account_type VARCHAR(50) NOT NULL UNIQUE,
  description VARCHAR(255) NOT NULL,
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
  description TEXT NOT NULL,
  address VARCHAR(255) NOT NULL,
  contact_number VARCHAR(20) NOT NULL,
  email VARCHAR(255) NOT NULL,
  logo VARCHAR(255),
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(company_id),
  FOREIGN KEY(account_id) REFERENCES user_account(account_id)
);

CREATE TABLE idp_category (
  category_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL UNIQUE,
  description VARCHAR(255) NOT NULL,
  is_suspended BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(category_id)
);

CREATE TABLE idp (
  idp_id INT NOT NULL AUTO_INCREMENT,
  account_id INT NOT NULL,
  category_id INT NOT NULL,
  title VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  location VARCHAR(255) NOT NULL,
  budget DECIMAL(12,2) NOT NULL,
  status ENUM('Current', 'Past') NOT NULL DEFAULT 'Current',
  images JSON,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(idp_id),
  FOREIGN KEY(account_id) REFERENCES user_account(account_id),
  FOREIGN KEY(category_id) REFERENCES idp_category(category_id)
);

CREATE TABLE favourite (
  favourite_id INT NOT NULL AUTO_INCREMENT,
  account_id INT NOT NULL,
  idp_id INT NOT NULL,
  saved_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(favourite_id),
  UNIQUE (account_id, idp_id),
  FOREIGN KEY(account_id) REFERENCES user_account(account_id),
  FOREIGN KEY(idp_id) REFERENCES idp(idp_id) ON DELETE CASCADE
);

CREATE TABLE idp_view (
  view_id INT NOT NULL AUTO_INCREMENT,
  idp_id INT NOT NULL,
  account_id INT NOT NULL,
  viewed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(view_id),
  FOREIGN KEY(idp_id) REFERENCES idp(idp_id) ON DELETE CASCADE,
  FOREIGN KEY(account_id) REFERENCES user_account(account_id)
);

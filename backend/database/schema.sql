CREATE DATABASE IF NOT EXISTS interior_design_platform
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE interior_design_platform;

CREATE TABLE user_profile (
  profile_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL UNIQUE,
  account_type ENUM('UserAdmin','InteriorDesigner','Customer','PlatformManager') NOT NULL,
  permissions TEXT NOT NULL,
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

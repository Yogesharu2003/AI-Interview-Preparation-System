CREATE DATABASE IF NOT EXISTS ai_interview_db;

USE ai_interview_db;

-- --------------------------------------------------------
-- Table: users
-- --------------------------------------------------------

CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id),
    UNIQUE KEY email (email)
);

-- --------------------------------------------------------
-- Table: admin
-- --------------------------------------------------------

CREATE TABLE admin (
    admin_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(100),
    password VARCHAR(100),
    fullname VARCHAR(100),
    email VARCHAR(100),
    PRIMARY KEY (admin_id),
    UNIQUE KEY email (email)
);

-- --------------------------------------------------------
-- Table: resumes
-- --------------------------------------------------------

CREATE TABLE resumes (
    resume_id INT NOT NULL AUTO_INCREMENT,
    fullname VARCHAR(100),
    email VARCHAR(100),
    resume_name VARCHAR(255),
    resume_path VARCHAR(255),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (resume_id)
);

-- --------------------------------------------------------
-- Table: interviews
-- --------------------------------------------------------

CREATE TABLE interviews (
    interview_id INT NOT NULL AUTO_INCREMENT,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    resume_name VARCHAR(255),
    total_questions INT DEFAULT 0,
    total_score INT DEFAULT 0,
    percentage DECIMAL(5,2) DEFAULT 0.00,
    interview_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (interview_id)
);

-- --------------------------------------------------------
-- Table: interview_answers
-- --------------------------------------------------------

CREATE TABLE interview_answers (
    answer_id INT NOT NULL AUTO_INCREMENT,
    fullname VARCHAR(100),
    question TEXT,
    answer TEXT,
    score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    correct_answer TEXT,
    feedback TEXT,
    interview_id INT,
    PRIMARY KEY (answer_id),
    KEY fk_interview (interview_id),
    CONSTRAINT fk_interview
        FOREIGN KEY (interview_id)
        REFERENCES interviews(interview_id)
        ON DELETE CASCADE
);
"""
All sql queries as constants
Authors: May Steinfeld & Sheryl Sitruk
"""

CREATE_DB = "CREATE DATABASE IF NOT EXISTS glassdoor;"
USE_DB = "USE glassdoor;"
CREATE_JOB_TABLE = """
        CREATE TABLE IF NOT EXISTS job (
        job_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        job_title varchar(255) NOT NULL,
        job_description text NOT NULL,
        job_location varchar(255) NOT NULL,
        job_publication_date date NOT NULL,
        company_id int NOT NULL
        );
        """

CREATE_COMPANY_TABLE = """
        CREATE TABLE IF NOT EXISTS company (
        company_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        company_name varchar(255) UNIQUE NOT NULL,
        company_size varchar(255),
        company_rating float,
        company_founded int,
        company_industry varchar(255),
        company_sector varchar(255),
        company_type varchar(255),
        company_revenue varchar(255),
        company_headquarters varchar(255)
        );
        """

CREATE_COMPETITOR_TABLE = """
        CREATE TABLE IF NOT EXISTS company_competitors (
        company_id int NOT NULL,
        competitor_id int NOT NULL
        );
        """

ALTER_JOB_TABLE_1 = "ALTER TABLE job ADD FOREIGN KEY (company_id) REFERENCES company (company_id);"

ALTER_JOB_TABLE_2 = "ALTER TABLE job ADD UNIQUE KEY (job_title,company_id,job_location);"

ALTER_COMPETITOR_TABLE_1 = "ALTER TABLE company_competitors ADD FOREIGN KEY (company_id) REFERENCES company (company_id);"

ALTER_COMPETITOR_TABLE_2 = "ALTER TABLE company_competitors ADD FOREIGN KEY (competitor_id) REFERENCES company (company_id);"

ALTER_COMPETITOR_TABLE_3 = "ALTER TABLE company_competitors ADD UNIQUE KEY (company_id,competitor_id);"

INSERT_COMPANY_TABLE = """INSERT INTO company (company_name, company_size, company_rating, 
            company_founded, company_industry, company_sector, company_type, company_revenue, 
            company_headquarters) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
            company_id=company_id """

INSERT_COMPETITOR_TABLE = """INSERT INTO company_competitors (company_id, competitor_id) 
            VALUES ((SELECT company_id FROM company WHERE
            company_name = % s), (SELECT company_id FROM company WHERE
            company_name = % s)) ON DUPLICATE KEY UPDATE 
            company_id=company_id """

INSERT_JOB_TABLE = """INSERT INTO job (job_title, job_description, job_location, 
            job_publication_date, company_id) VALUES (%s, %s, %s, %s, (SELECT company_id FROM company WHERE 
            company_name = %s)) ON DUPLICATE KEY UPDATE job_id=job_id """

GET_COMPANY = """(SELECT company_id FROM company WHERE company_name = %s)"""

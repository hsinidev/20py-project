-- Digital Footprint Intelligence Hub - Database Schema
-- Developed by HSINI MOHAMED

CREATE TABLE IF NOT EXISTS investigations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS discovered_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id INTEGER,
    platform TEXT NOT NULL,
    url TEXT NOT NULL,
    status_code INTEGER,
    metadata TEXT,
    found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);

CREATE TABLE IF NOT EXISTS dork_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id INTEGER,
    query TEXT NOT NULL,
    result_url TEXT NOT NULL,
    title TEXT,
    snippet TEXT,
    found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);

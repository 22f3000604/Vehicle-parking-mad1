#!/usr/bin/env python3
"""
Migration script to add email verification columns to User table
"""

import sqlite3
import os

def migrate_database():
    db_path = '/workspaces/Vehicle-parking-mad1/instance/site.db'
    
    if not os.path.exists(db_path):
        print("Database file not found!")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add is_verified column if it doesn't exist
        if 'is_verified' not in columns:
            cursor.execute('ALTER TABLE user ADD COLUMN is_verified BOOLEAN DEFAULT 0 NOT NULL')
            print("Added 'is_verified' column")
        else:
            print("'is_verified' column already exists")
        
        # Add verification_token column if it doesn't exist
        if 'verification_token' not in columns:
            cursor.execute('ALTER TABLE user ADD COLUMN verification_token TEXT')
            print("Added 'verification_token' column")
        else:
            print("'verification_token' column already exists")
        
        # Add created_at column if it doesn't exist
        if 'created_at' not in columns:
            cursor.execute('ALTER TABLE user ADD COLUMN created_at DATETIME')
            print("Added 'created_at' column")
        else:
            print("'created_at' column already exists")
        
        # Commit changes
        conn.commit()
        print("Database migration completed successfully!")
        
        # Verify the changes
        cursor.execute("PRAGMA table_info(user)")
        columns_after = [column[1] for column in cursor.fetchall()]
        print(f"User table columns: {columns_after}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Migration failed: {e}")
        if conn:
            conn.close()
        return False

if __name__ == "__main__":
    migrate_database()

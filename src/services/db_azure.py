import pyodbc
import json
from datetime import datetime
from datetime import time
from pydantic import BaseModel
from typing import Optional, Dict

# Define connection string for Azure SQL Database
connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:physician.database.windows.net,1433;Database=biov2;Uid=chinmay;Pwd=babu@0603;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Example Pydantic models for input data
class User(BaseModel):
    first_name: str
    last_name: str
    interests: Optional[str] = None
    writing_style: Optional[str] = None
    tone: Optional[str] = None
    structure: Optional[str] = None
    writing_influences: Optional[str] = None
    post_days: Optional[str] = None
    # start_time: Optional[datetime] = None
    # end_time: Optional[datetime] = None
    start_time: Optional[time] = None  # Changed to time
    end_time: Optional[time] = None    # Changed to time

class PreviewPost(BaseModel):
    user_id: int
    topic: str
    generated_content: Optional[str] = None

class LinkedInProfile(BaseModel):
    name: str
    sub: str
    locale: Dict
    given_name: str
    family_name: str
    picture: Optional[str] = None

# CRUD operations for Users
def add_user(user_data: User):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (first_name, last_name, interests, writing_style, tone, structure, writing_influences, post_days, start_time, end_time, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_data.first_name,
            user_data.last_name,
            user_data.interests if user_data.interests else None,  # Handle None values
            user_data.writing_style if user_data.writing_style else None,
            user_data.tone if user_data.tone else None,
            user_data.structure if user_data.structure else None,
            user_data.writing_influences if user_data.writing_influences else None,
            user_data.post_days if user_data.post_days else None,
            user_data.start_time if user_data.start_time else None,
            user_data.end_time if user_data.end_time else None,
            datetime.utcnow(),
            datetime.utcnow()
        ))
        conn.commit()
        return cursor.execute("SELECT @@IDENTITY AS id").fetchone().id


# CRUD operations for PreviewPosts
def add_preview_post(post_data: PreviewPost):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO preview_posts (user_id, topic, generated_content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            post_data.user_id,
            post_data.topic,
            post_data.generated_content if post_data.generated_content else None,  # Handle None values
            datetime.utcnow(),
            datetime.utcnow()
        ))
        conn.commit()
        return cursor.execute("SELECT @@IDENTITY AS id").fetchone().id


# CRUD operations for LinkedIn Profiles
def add_linkedin_profile(profile_data: LinkedInProfile):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO linkedin_profiles (name, sub, locale, given_name, family_name, picture, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile_data.name,
            profile_data.sub,
            json.dumps(profile_data.locale),  # Converts dict to JSON string
            profile_data.given_name,
            profile_data.family_name,
            profile_data.picture if profile_data.picture else None,
            datetime.utcnow(),
            datetime.utcnow()
        ))
        conn.commit()
        # Use SCOPE_IDENTITY() instead of @@IDENTITY to get the correct ID
        cursor.execute("SELECT SCOPE_IDENTITY() AS id")
        new_id = cursor.fetchone().id
        return new_id




# Example usage - Connecting to the database and adding data
if __name__ == "__main__":
    # Example: Add a new user
    new_user = User(
        first_name="Alice",
        last_name="Smith",
        interests="Technology, AI",
        writing_style="Formal",
        tone="Professional",
        structure="Concise",
        writing_influences="Isaac Asimov",
        post_days="Monday, Wednesday",
        start_time=datetime.strptime("12:09", "%H:%M").time(),
        end_time=datetime.strptime("10:00", "%H:%M").time()
    )
    added_user_id = add_user(new_user)
    print(f"User added with ID: {added_user_id}")

    # Example: Add a preview post for the user
    post_data = PreviewPost(
        user_id=added_user_id,
        topic="AI in 2025",
        generated_content="This post talks about the future of AI in 2025..."
    )
    added_post_id = add_preview_post(post_data)
    print(f"Post added with ID: {added_post_id}")

    # Example: Add a LinkedIn profile
    profile_data = LinkedInProfile(
        name="Alice Smith",
        sub="abc123",
        locale={"country": "US", "language": "en"},
        given_name="Alice",
        family_name="Smith",
        picture="https://example.com/profile.jpg"
    )
    added_profile_id = add_linkedin_profile(profile_data)
    print(f"LinkedIn Profile added with ID: {added_profile_id}")

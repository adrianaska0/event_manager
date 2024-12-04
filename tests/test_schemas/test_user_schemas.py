from builtins import str
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest
import uuid
from app.utils.nickname_gen import generate_nickname

# Example data
user_base_data = {
    "email": "john.doe@example.com",
    "nickname": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Experienced software developer specializing in web applications.",
    "profile_picture_url": "https://example.com/profiles/john.jpg",
    "linkedin_profile_url": "https://linkedin.com/in/johndoe",
    "github_profile_url": "https://github.com/johndoe"
}

user_create_data = {
    "email": "john.doe@example.com",
    "password": "Secure*1234",
    "nickname": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Experienced software developer specializing in web applications.",
    "profile_picture_url": "https://example.com/profiles/john.jpg",
    "linkedin_profile_url": "https://linkedin.com/in/johndoe",
    "github_profile_url": "https://github.com/johndoe"
}

user_update_data = {
    "email": "john.doe@example.com",
    "nickname": "john_doe123",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Experienced software developer specializing in web applications.",
    "profile_picture_url": "https://example.com/profiles/john.jpg",
    "linkedin_profile_url": "https://linkedin.com/in/johndoe",
    "github_profile_url": "https://github.com/johndoe"
}

user_response_data = {
    "id": uuid.uuid4(),
    "role": "AUTHENTICATED",
    "email": "john.doe@example.com",
    "nickname": generate_nickname(),
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Experienced software developer specializing in web applications.",
    "profile_picture_url": "https://example.com/profiles/john.jpg",
    "linkedin_profile_url": "https://linkedin.com/in/johndoe",
    "github_profile_url": "https://github.com/johndoe",
    "is_professional": True
}

login_request_data = {
    "email": "john.doe@example.com",
    "password": "Secure*1234"
}

user_base_data_invalid = {
    "email": "john.doe.example.com",
    "nickname": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Experienced software developer specializing in web applications.",
    "profile_picture_url": "https://example.com/profiles/john.jpg",
    "linkedin_profile_url": "https://linkedin.com/in/johndoe",
    "github_profile_url": "https://github.com/johndoe"
}

# Helper function to reset user_base_data to a valid state
def reset_user_base_data():
    return {
        "email": "john.doe@example.com",
        "nickname": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "Experienced software developer specializing in web applications.",
        "profile_picture_url": "https://example.com/profiles/john.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe"
    }

# Tests for UserBase
def test_user_base_valid():
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data.get("nickname")
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid():
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data.get("nickname")
    assert user.password == user_create_data["password"]

# Tests for UserUpdate
def test_user_update_valid():
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.first_name == user_update_data.get("first_name")

# Tests for UserResponse
def test_user_response_valid():
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]

# Tests for LoginRequest
def test_login_request_valid():
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["john_doe", "john-doe", "john_doe123", "123john"])
def test_user_base_nickname_valid(nickname):
    data = reset_user_base_data()
    data["nickname"] = nickname
    user = UserBase(**data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["john doe", "john?doe", "", "jo"])
def test_user_base_nickname_invalid(nickname):
    data = reset_user_base_data()
    data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url):
    data = reset_user_base_data()
    data["profile_picture_url"] = url
    user = UserBase(**data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url):
    data = reset_user_base_data()
    data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**data)

# Tests for invalid email
def test_user_base_invalid_email():
    with pytest.raises(ValidationError) as exc_info:
        UserBase(**user_base_data_invalid)
    
    assert "value is not a valid email address" in str(exc_info.value)
    assert "john.doe.example.com" in str(exc_info.value)

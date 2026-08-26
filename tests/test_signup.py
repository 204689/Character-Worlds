from playwright.sync_api import Page
from app.models import UserProfile
from tests.pages.auth import SignupPage

def test_signup(page: Page, user_data: dict):
    page.goto("/")
    signup_page = SignupPage(page)
    signup_page.complete_signup_form(user_data["username"], user_data["password"])

    user = UserProfile.objects.get(username=user_data["username"])
    assert user.username == user_data["username"]
    assert user.check_password(user_data["password"])

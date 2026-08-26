from playwright.sync_api import Page

class SignupPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_field = page.get_by_placeholder("Username")
        self.password_field = page.locator('input[name="password1"]')
        self.password_confirmation_field = page.locator('input[name="password2"]')
        self.signup_button = page.get_by_role("button", name="Create your account")

    def complete_signup_form(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.password_confirmation_field.fill(password)
        self.signup_button.click()

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_field = page.get_by_placeholder("Username")
        self.password_field = page.get_by_placeholder("Password")
        self.signup_button = page.get_by_role("button", name="Sign in")



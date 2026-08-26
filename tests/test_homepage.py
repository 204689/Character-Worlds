from playwright.sync_api import Page

def test_can_load_homepage(page: Page):
    page.goto("/")
    assert "Write and collaborate" in page.content()

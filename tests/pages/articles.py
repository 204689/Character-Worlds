from playwright.sync_api import Page

class ArticlesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.start_new_article_button = page.get_by_role("link", name="Start new article")
        self.search_input = page.get_by_placeholder("Search for articles")
        self.search_button = page.get_by_role("button", name="Search")
        self.clear_search_button = page.get_by_role("link", name="Clear search")

        # Text elements
        self.welcome_heading = page.get_by_role("heading", name="Welcome")
        self.no_articles_message = page.get_by_text("There are no articles yet.")

class ArticlePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title_input = page.get_by_placeholder("Write a title for your article")
        self.status_select = page.locator("#id_status")
        self.content_editor = page.locator("#id_content")
        self.code_mirror_editor = page.locator(".CodeMirror-scroll")
        self.twitter_post_input = page.locator("#id_twitter_post")

        self.save_button = page.get_by_role("button", name="Save")

    def set_status(self, status: str):
        self.status_select.select_option(status)

    def fill_article_content(self, content: str):
        self.code_mirror_editor.click()
        self.page.keyboard.insert_text(content)

    def fill_article(
            self, title: str, content: str, twitter_post: str = "", status: str = "draft"
    ):
        self.title_input.fill(title)
        self.set_status(status)
        self.fill_article_content(content)
        self.twitter_post_input.fill(twitter_post)

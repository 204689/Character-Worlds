from playwright.sync_api import Page
import pytest
from app.models import Article
from tests.pages.articles import ArticlesPage, ArticlePage

@pytest.fixture
def created_articles(verified_user):
    Article.objects.create(title = "Test Article", content = "This is a test article", creator = verified_user, status = "published")
    Article.objects.create(title = "Test Article 2", content = "This is a test article", creator = verified_user, status = "published")


def test_empty_articles_page(auth_page: Page):
    auth_page.goto("/articles/")
    articles_page = ArticlesPage(auth_page)
    assert articles_page.no_articles_message.is_visible()

def test_search_articles(auth_page: Page, created_articles):
    auth_page.goto("/articles/")
    articles_page = ArticlesPage(auth_page)

    articles_page.search_input.fill("2")
    articles_page.search_button.click()

    assert articles_page.page.get_by_text("Test Article", exact = True).is_hidden()
    assert articles_page.page.get_by_text("Test Article 2", exact = True).is_visible()

def test_clear_search_articles(auth_page: Page, created_articles):
    auth_page.goto("/articles/")
    articles_page = ArticlesPage(auth_page)

    articles_page.search_input.fill("2")
    articles_page.search_button.click()
    articles_page.clear_search_button.click()

    assert articles_page.page.get_by_text("Test Article", exact = True).is_visible()
    assert articles_page.page.get_by_text("Test Article 2", exact = True).is_visible()

def test_visible_articles(auth_page: Page, created_articles):
    auth_page.goto("/articles/")
    articles_page = ArticlesPage(auth_page)

    assert articles_page.page.get_by_text("Test Article", exact = True).is_visible()
    assert articles_page.page.get_by_text("Test Article 2", exact = True).is_visible()


def test_create_article(auth_page: Page):
    article_title = "The First Article"

    auth_page.goto("/articles/create/")
    article_page = ArticlePage(auth_page)

    article_page.fill_article(
        title = article_title,
        content = "This is the content",
        twitter_post = "Check out my test!",
        status = "published",
    )
    article_page.save_button.click()

    articles_page = ArticlesPage(auth_page)
    assert articles_page.page.get_by_text("The First Article", exact = True).is_visible()

def test_create_edit_article(auth_page: Page):
    article_title = "The Second Article"

    auth_page.goto("/articles/create/")
    article_page = ArticlePage(auth_page)

    article_page.fill_article(
        title = article_title,
        content = "This is the content2",
        twitter_post = "Check out my test!",
        status = "published",
    )
    article_page.save_button.click()

    articles_page = ArticlesPage(auth_page)
    articles_page.page.get_by_text(article_title, exact = True).click()

    article_page = ArticlePage(auth_page)

    assert (
        "This is the content2"
        in article_page.content_editor.text_content()
    )

    article_title = "The Second Article 2.0"

    article_page.fill_article(
        title = article_title,
        content = " Have a good day!",
        status = "published"
    )

    article_page.save_button.click()

    articles_page = ArticlesPage(auth_page)
    assert articles_page.page.get_by_text(article_title, exact = True).is_visible()


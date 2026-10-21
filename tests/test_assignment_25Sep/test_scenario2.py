#Scenario 2: Amazon – Left Navigation Headings
from playwright.sync_api import Page
def test_amazon_menu(page: Page):
    page.goto("https://www.amazon.in/")
    page.locator("//a[@id='nav-hamburger-menu']").click()
    print(page.url)
    print(page.locator("//*[contains(@id,'hmenu')]").count())
    print(page.locator("//*[@id='nav-hamburger-menu']").count())
    print(page.locator("body").inner_text()[:3000])
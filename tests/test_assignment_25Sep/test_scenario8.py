#Scenario 8: Amazon – Navigation Menu Subcategories
from playwright.sync_api import Page
def test_amazon_diagnostic(page: Page):
    page.goto("https://www.amazon.in/",wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    print(page.url)
    print(page.title())
    print(page.locator("body").inner_text()[:5000])
    print(page.locator("[id]").evaluate_all("""elements => elements.slice(0, 100).map(e => ({tag: e.tagName,id: e.id,text: (e.innerText || '').trim()}))"""))
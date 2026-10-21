#Scenario 4: Amazon – Product Name and Price
from playwright.sync_api import Page
def test_product_price_by_name(page: Page):
    page.goto("https://www.amazon.in/")
    search_box = page.locator("#twotabsearchtextbox")
    search_box.fill("wireless mouse")
    search_box.press("Enter")
    products = page.locator("//div[@data-component-type='s-search-result']""[.//h2]")
    print("Number of product containers:", products.count())
    for product in products.all():
        name = product.locator("xpath=.//h2//span").inner_text()
        print("Product:", name)

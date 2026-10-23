#Scenario 4: Amazon – Product Name and Price

from playwright.sync_api import Page, expect


def test_product_price_by_name(page: Page):

    page.goto("https://www.amazon.in/", wait_until="domcontentloaded")

    search_box = page.locator("#twotabsearchtextbox")
    expect(search_box).to_be_visible(timeout=15000)

    search_box.fill("wireless mouse")
    search_box.press("Enter")

    page.wait_for_url("**/s/**", timeout=20000)

    products = page.locator("div[data-component-type='s-search-result']:has(h2)")

    expect(products.first).to_be_visible(timeout=20000)

    product_count = products.count()
    print("Number of product containers:", product_count)

    for product in products.all():
        name_locator = product.locator("h2 a span").first
        price_locator = product.locator(".a-price .a-offscreen").first

        if name_locator.count() > 0:
            product_name = name_locator.inner_text().strip()

            if price_locator.count() > 0:
                product_price = price_locator.inner_text().strip()
            else:
                product_price = "Price not displayed"

            print("Product:", product_name)
            print("Price:", product_price)
            print("-" * 50)

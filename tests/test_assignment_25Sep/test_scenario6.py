#Scenario 6: Amazon – Search Results
from playwright.sync_api import Page
def test_book_price_and_add_to_cart(page: Page):
    page.goto("https://www.amazon.in/", wait_until="domcontentloaded")
    search_text = "The Howl A Tale of Love Power and Revenge"
    search_box = page.locator("#twotabsearchtextbox")
    search_box.fill(search_text)
    search_box.press("Enter")
    page.wait_for_load_state("domcontentloaded")
    expected_title = ("The Howl -A Tale of Love, Power and Revenge")
    products = page.locator("div[data-component-type='s-search-result']")
    matching_product = None
    for product in products.all():
        title_locator = product.locator("h2")
        if title_locator.count() == 0:
            continue
        actual_title = title_locator.inner_text().strip()
        normalized_actual = " ".join(actual_title.split())
        normalized_expected = " ".join(expected_title.split())
        if normalized_actual.lower() == normalized_expected.lower():
            matching_product = product
            break
    assert matching_product is not None, (f"Book '{expected_title}' was not found.")
    product_name = matching_product.locator("h2").inner_text()
    print("Product name:", product_name)
    price = matching_product.locator("xpath=.//span[contains(@class,'a-price')]""//span[contains(@class,'a-offscreen')]")
    assert price.count() > 0, (f"Price not found for '{product_name}'.")
    product_price = price.all_inner_texts()[0]
    print("Product price:", product_price)
    add_to_cart = matching_product.locator("xpath=.//input[@value='Add to cart']")
    if add_to_cart.count() == 0:
        add_to_cart = matching_product.locator("xpath=.//button[contains(""translate(normalize-space(),""'ABCDEFGHIJKLMNOPQRSTUVWXYZ',""'abcdefghijklmnopqrstuvwxyz'),""'add to cart'"")]")
    if add_to_cart.count() == 0:
        add_to_cart = matching_product.locator("[name='submit.addToCart']")
    if add_to_cart.count() > 0:
        print("Add to Cart found in the product container")
        add_to_cart.click()
        print("Product added to cart")
        return
    print("Add to Cart is not available directly ""in the search-result card.")
    product_links = matching_product.locator("a[href]")
    product_url = None
    for link in product_links.all():
        href = link.get_attribute("href")
        if not href:
            continue
        if "/dp/" in href or "/gp/" in href:
            product_url = href
            break
    assert product_url is not None, (f"Product link not found for '{product_name}'.")
    if product_url.startswith("/"):
        product_url = "https://www.amazon.in" + product_url
    page.goto(product_url,wait_until="domcontentloaded")
    detail_title = page.locator("#productTitle")
    assert detail_title.count() > 0, ("Product detail page was not opened.")
    detail_name = detail_title.inner_text().strip()
    print("Product detail name:", detail_name)
    detail_add_to_cart = page.locator("#add-to-cart-button")
    assert detail_add_to_cart.count() > 0, (f"Add to Cart is not available for '{detail_name}'.")
    print("Add to Cart found")
    detail_add_to_cart.click()
    print("Product added to cart")
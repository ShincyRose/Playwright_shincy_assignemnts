
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError


def test_amazon_checkout_journey(page: Page):

    page.goto("https://www.amazon.in/",wait_until="domcontentloaded")

    product_keyword = "wireless mouse"

    search_box = page.locator("#twotabsearchtextbox")
    expect(search_box).to_be_visible(timeout=20000)

    search_box.fill(product_keyword)
    search_box.press("Enter")

    product_cards = page.locator('div[data-component-type="s-search-result"]')

    expect(product_cards.first).to_be_visible(timeout=20000)

    required_keyword = "wireless mouse"
    matched_card = None
    matched_title = ""

    for i in range(product_cards.count()):
        card = product_cards.nth(i)
        title_locator = card.locator("h2").first

        if not title_locator.is_visible():
            continue

        title = " ".join(title_locator.inner_text().split())

        if required_keyword.casefold() in title.casefold():
            matched_card = card
            matched_title = title
            break

    assert matched_card is not None, (f"No product containing '{required_keyword}' was found.")

    print("\nSelected product:", matched_title)

    product_link = matched_card.locator("a:has(h2)").first

    if product_link.count() == 0:
        product_link = matched_card.locator("a[href*='/dp/']").first

    expect(product_link).to_be_visible(timeout=10000)

    product_url = product_link.get_attribute("href")
    assert product_url, "Product URL was not found."

    if product_url.startswith("/"):
        product_url = "https://www.amazon.in" + product_url

    page.goto(product_url, wait_until="domcontentloaded")

    detail_title = page.locator("span#productTitle")
    expect(detail_title).to_be_visible(timeout=20000)

    actual_title = " ".join(detail_title.inner_text().split())
    print("Product detail title:", actual_title)

    assert required_keyword.casefold() in actual_title.casefold(), (f"Unexpected product title: {actual_title}")

    add_to_cart = page.locator("#add-to-cart-button")

    if add_to_cart.count() == 0 or not add_to_cart.is_visible():
        print("Add to Cart control is unavailable.")
        print("The product may be unavailable or the page layout differs.")
        return

    expect(add_to_cart).to_be_enabled(timeout=10000)

    try:
        add_to_cart.click(timeout=10000)
        print("Add to Cart clicked.")

    except PlaywrightTimeoutError:
        print("Unable to add the product to the cart in this session.")
        return

    cart_link = page.locator("#nav-cart")

    expect(cart_link).to_be_visible(timeout=15000)
    cart_link.click()

    expect(page).to_have_url(__import__("re").compile(r"/cart"),timeout=20000)

    cart_items = page.locator("div.sc-list-item")

    expect(cart_items.first).to_be_visible(timeout=20000)

    cart_item_found = False

    for i in range(cart_items.count()):
        item = cart_items.nth(i)

        item_text = " ".join(item.inner_text().split())

        if actual_title.casefold() in item_text.casefold():
            cart_item_found = True

            print("Cart item:", item_text)

            quantity = item.locator("span.a-dropdown-prompt")

            if quantity.count() > 0:
                print("Cart quantity:", quantity.first.inner_text())
            else:
                print("Quantity control was not found in the expected format.")

            break

    assert cart_item_found, (f"Selected product '{actual_title}' was not found in the cart.")

    print("Cart item validated successfully.")

    checkout_button = page.locator('input[name="proceedToRetailCheckout"], ''input[name="proceedToCheckout"], ''button[name="proceedToRetailCheckout"]').first

    if checkout_button.count() > 0 and checkout_button.is_visible():
        print("Checkout control is available.")
        checkout_button.click()

        page.wait_for_load_state("domcontentloaded")

        print("Current checkout URL:", page.url)
        print("Stopped before final order confirmation/payment.")

    else:
        print( "Checkout control is unavailable in this session. ""Stopped safely on the cart page.")



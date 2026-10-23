
import re
import pytest
from playwright.sync_api import Page, expect


def test_conditional_add_to_cart(page: Page):

    page.goto("https://www.amazon.in/",wait_until="domcontentloaded")

    search_keyword = "wireless mouse"

    search_box = page.locator("#twotabsearchtextbox")
    expect(search_box).to_be_visible(timeout=20000)

    search_box.fill(search_keyword)
    search_box.press("Enter")

    cards = page.locator('div[data-component-type="s-search-result"]')
    expect(cards.first).to_be_visible(timeout=20000)

    required_keyword = "wireless mouse"
    matched_card = None
    matched_title = ""

    for i in range(cards.count()):
        card = cards.nth(i)
        title_locator = card.locator("h2").first

        if not title_locator.is_visible():
            continue

        title = " ".join(title_locator.inner_text().split())

        if required_keyword.casefold() in title.casefold():
            matched_card = card
            matched_title = title
            break

    assert matched_card is not None, (
        f"No product matching '{required_keyword}' was found."
    )

    print("\nSelected product:", matched_title)

    product_link = matched_card.locator("a:has(h2)").first

    if product_link.count() == 0:
        product_link = matched_card.locator("a[href*='/dp/']").first

    expect(product_link).to_be_visible(timeout=10000)

    product_href = product_link.get_attribute("href")
    assert product_href, "Product detail URL was not found."

    if product_href.startswith("/"):
        product_href = "https://www.amazon.in" + product_href

    page.goto(product_href, wait_until="domcontentloaded")


    title_locator = page.locator("span#productTitle")
    expect(title_locator).to_be_visible(timeout=20000)

    product_title = " ".join(title_locator.inner_text().split())
    print("Product detail title:", product_title)


    availability = page.locator("#availability")
    availability_text = ""

    if availability.count() > 0 and availability.is_visible():
        availability_text = " ".join(availability.inner_text().split())

    print("Availability message:", availability_text or "Not displayed")

 
    add_to_cart = page.locator("#add-to-cart-button")

    control_visible = (add_to_cart.count() > 0 and add_to_cart.is_visible())

    control_enabled = (control_visible and add_to_cart.is_enabled())

    print("Add to Cart visible:", control_visible)
    print("Add to Cart enabled:", control_enabled)

    unavailable_words = ("currently unavailable","out of stock","temporarily out of stock",)

    availability_indicates_unavailable = any(word in availability_text.casefold() for word in unavailable_words)

    if availability_indicates_unavailable:
        reason = ("The product availability message indicates it is unavailable: "+ availability_text)

    elif not control_visible:
        reason = "The Add to Cart control is missing or not visible."

    elif not control_enabled:
        reason = "The Add to Cart control is disabled."

    else:
        reason = ""

    if reason:
        print("\nPRODUCT UNAVAILABLE FOR THIS TEST")
        print("Product:", product_title)
        print("Reason:", reason)

        pytest.skip(f"Cart validation skipped for '{product_title}'. {reason}")

    expect(add_to_cart).to_be_enabled()
    add_to_cart.click()

    print("Product added to cart.")


    cart_link = page.locator("#nav-cart")
    expect(cart_link).to_be_visible(timeout=15000)
    cart_link.click()

    expect(page).to_have_url(re.compile(r"/cart"),timeout=20000)

    cart_items = page.locator("div.sc-list-item")
    expect(cart_items.first).to_be_visible(timeout=20000)

    matching_item_found = False

    for i in range(cart_items.count()):
        item = cart_items.nth(i)
        item_text = " ".join(item.inner_text().split())

        if product_title.casefold() in item_text.casefold():
            matching_item_found = True
            print("Cart item validated:", item_text)
            break

    assert matching_item_found, (f"Product was added, but '{product_title}' ""was not found in the cart.")


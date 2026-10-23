
import re
from playwright.sync_api import Page, expect


def normalize_text(value):
    return " ".join(value.split()).casefold()


def test_product_state_across_pages(page: Page):

    page.goto("https://www.amazon.in/",wait_until="domcontentloaded")

    search_keyword = "wireless mouse"

    search_box = page.locator("#twotabsearchtextbox")
    expect(search_box).to_be_visible(timeout=20000)

    search_box.fill(search_keyword)
    search_box.press("Enter")

    product_cards = page.locator('div[data-component-type="s-search-result"]')

    expect(product_cards.first).to_be_visible(timeout=20000)

    required_keyword = "wireless mouse"
    selected_card = None
    selected_title = ""

    for i in range(product_cards.count()):
        card = product_cards.nth(i)
        title_locator = card.locator("h2").first

        if not title_locator.is_visible():
            continue

        title = " ".join(title_locator.inner_text().split())

        if required_keyword.casefold() in title.casefold():
            selected_card = card
            selected_title = title
            break

    assert selected_card is not None, (f"No product containing '{required_keyword}' was found.")

    stored_title = selected_title
    stored_search_keyword = search_keyword

    product_link = selected_card.locator("a:has(h2)").first

    if product_link.count() == 0:
        product_link = selected_card.locator("a[href*='/dp/']").first

    expect(product_link).to_be_visible(timeout=10000)

    product_href = product_link.get_attribute("href")

    assert product_href, "Selected product URL is missing."

    product_id_match = re.search( r"/dp/([A-Z0-9]{10})",product_href)

    assert product_id_match is not None, (f"Could not capture product ID from URL: {product_href}")

    stored_product_id = product_id_match.group(1)

    print("\nStored search keyword:", stored_search_keyword)
    print("Stored product title:", stored_title)
    print("Stored product ID:", stored_product_id)

    if product_href.startswith("/"):
        product_url = "https://www.amazon.in" + product_href
    else:
        product_url = product_href

    page.goto(product_url,wait_until="domcontentloaded")

    detail_title = page.locator("span#productTitle")
    expect(detail_title).to_be_visible(timeout=20000)

    actual_title = " ".join(detail_title.inner_text().split())

    assert normalize_text(stored_title) == normalize_text(actual_title), (f"Product title changed after navigation!\n"f"Stored title: {stored_title}\n"f"Detail title: {actual_title}")

    print("PASS: Product title retained on detail page.")

    current_id_match = re.search(r"/dp/([A-Z0-9]{10})",page.url)

    assert current_id_match is not None, ("Product ID was not found in the detail page URL.")

    assert current_id_match.group(1) == stored_product_id, (f"Product ID changed!\n"f"Stored ID: {stored_product_id}\n"f"Current ID: {current_id_match.group(1)}")

    print("PASS: Product identifier retained.")

    add_to_cart = page.locator("#add-to-cart-button")

    expect(add_to_cart).to_be_visible(timeout=15000)
    expect(add_to_cart).to_be_enabled(timeout=10000)
    add_to_cart.click()

    print("Add to Cart clicked.")

    cart_link = page.locator("#nav-cart")
    expect(cart_link).to_be_visible(timeout=15000)
    cart_link.click()

    expect(page).to_have_url(re.compile(r"/cart"),timeout=20000)

    cart_items = page.locator("div.sc-list-item")

    expect(cart_items.first).to_be_visible(timeout=20000)

    matching_cart_item = False

    for i in range(cart_items.count()):
        item = cart_items.nth(i)
        item_text = " ".join(item.inner_text().split())

        if normalize_text(actual_title) in normalize_text(item_text):
            matching_cart_item = True
            print("Cart item found:", item_text)
            break

    assert matching_cart_item, (f"State loss: product '{stored_title}' "f"(ID: {stored_product_id}) was not found in the cart.")

    print("PASS: Same product found in the cart.")

    page.go_back(wait_until="domcontentloaded")

    search_url = ("https://www.amazon.in/s?k="+ stored_search_keyword.replace(" ", "+"))

    page.goto(search_url, wait_until="domcontentloaded")

    expect(page.locator('div[data-component-type="s-search-result"]').first).to_be_visible(timeout=20000)

    restored_search_box = page.locator("#twotabsearchtextbox")

    expect(restored_search_box).to_be_visible(timeout=10000)

    restored_keyword = restored_search_box.input_value()

    assert normalize_text(restored_keyword) == normalize_text(stored_search_keyword), (f"Search context was lost!\n"f"Expected: {stored_search_keyword}\n"f"Actual: {restored_keyword}")

    print("PASS: Search keyword restored:", restored_keyword)
    print("Stored product ID:", stored_product_id)
    print("Stored product title:", stored_title)

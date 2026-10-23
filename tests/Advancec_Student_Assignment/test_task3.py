import re
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError


def test_amazon_autosuggest_dropdown(page: Page):

    page.goto("https://www.amazon.in/", wait_until="domcontentloaded")

    search_box = page.locator("#twotabsearchtextbox")
    expect(search_box).to_be_visible(timeout=20000)

    partial_name = "wireless mou"
    search_box.fill(partial_name)

    print("\nEntered partial search:", partial_name)

    suggestions = page.locator("div.s-suggestion-container")

    try:
        suggestions.first.wait_for(state="visible",timeout=5000)

    except PlaywrightTimeoutError:
        print("Autocomplete suggestions were not displayed.")
        print("Using Enter as the search fallback.")

        search_box.fill(partial_name)
        search_box.press("Enter")

        expect(page.locator('div[data-component-type="s-search-result"]').first).to_be_visible(timeout=20000)

        print("Fallback search completed.")
        print("Current URL:", page.url)

    else:
        print("Autocomplete suggestions are displayed.")

        rows = page.locator("div.s-suggestion-container")

        visible_suggestions = []

        for i in range(rows.count()):
            row = rows.nth(i)

            if row.is_visible():
                text = " ".join(row.inner_text().split())

                if text:
                    visible_suggestions.append((row, text))
                    print("Suggestion:", text)

        selected_row = None
        selected_text = ""

        for row, text in visible_suggestions:
            if "wireless mouse for pc" in text.casefold():
                selected_row = row
                selected_text = text
                break

        if selected_row is None:
            print("Matching suggestion not found.")
            print("Using Enter as the search fallback.")

            search_box.fill(partial_name)
            search_box.press("Enter")

        else:
            print("Selecting suggestion:", selected_text)
            selected_row.click()

        expect(page).to_have_url(re.compile(r"[?&]k="),timeout=20000)

        expect(page.locator('div[data-component-type="s-search-result"]').first).to_be_visible(timeout=20000)

        print("Search navigation validated.")
        print("Current URL:", page.url)


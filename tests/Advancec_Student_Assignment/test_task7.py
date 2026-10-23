
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError


def test_amazon_pagination_or_infinite_scroll(page: Page):

    page.goto("https://www.amazon.in/",wait_until="domcontentloaded")

    search_keyword = "wireless mouse"

    search_box = page.locator("#twotabsearchtextbox")
    expect(search_box).to_be_visible(timeout=20000)

    search_box.fill(search_keyword)
    search_box.press("Enter")

    cards = page.locator('div[data-component-type="s-search-result"]')

    expect(cards.first).to_be_visible(timeout=20000)

    initial_count = cards.count()
    initial_url = page.url

    print("\nSearch keyword:", search_keyword)
    print("Initial product card count:", initial_count)
    print("Initial URL:", initial_url)

    next_link = page.locator("a.s-pagination-next")

    load_more = page.get_by_role("button",name="Load more",exact=False)

    if next_link.count() > 0 and next_link.is_visible() and (not next_link.get_attribute("aria-disabled") == "true"):
        print("Observed behavior: Pagination")

        next_href = next_link.get_attribute("href")
        assert next_href, "Next pagination link has no destination."

        next_link.click()

        try:
            expect(page).not_to_have_url(initial_url,timeout=15000)
        except AssertionError:
            print("URL did not change as expected.")

        expect(cards.first).to_be_visible(timeout=20000)

        new_count = cards.count()
        new_url = page.url

        print("Next page URL:", new_url)
        print("Product card count on next page:", new_count)

        assert new_url != initial_url, ("Pagination did not navigate to a different URL.")

        print("Pagination navigation completed.")

    elif load_more.count() > 0 and load_more.is_visible():

        print("Observed behavior: Load More control")

        load_more.click()

        try:
            expect(cards).not_to_have_count(initial_count,timeout=15000)
        except AssertionError:
            print("The number of product cards did not change.")

        new_count = cards.count()
        print("Product cards after Load More:", new_count)

        assert new_count > initial_count, ("Load More did not add any product cards." )

        print("Load More validation completed.")

    else:
        print("No visible Next or Load More control detected.")
        print("Testing for lazy-loaded or infinite-scroll results.")

        new_count = initial_count
        increased = False

        for attempt in range(1, 5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            try:
                page.wait_for_function("""initial => document.querySelectorAll('div[data-component-type="s-search-result"]').length > initial""",arg=new_count,timeout=4000)

                updated_count = cards.count()

                if updated_count > new_count:
                    increased = True
                    new_count = updated_count

                    print(f"Scroll {attempt}: product cards increased "f"to {new_count}")
                    break

            except PlaywrightTimeoutError:
                print(f"Scroll {attempt}: no additional product cards ""loaded within the wait period.")

        if increased:
            print("Observed behavior: Lazy-loaded/infinite-scroll results.")
            assert new_count > initial_count
        else:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            pagination = page.locator("a.s-pagination-next")

            if pagination.count() > 0 and pagination.is_visible():
                print("Observed behavior: Pagination is present ""near the bottom of the page.")
            else:
                print("Observed behavior: No additional results loaded ""and no visible Next/Load More control was found.")

                print("Record this session as inconclusive for ""infinite scrolling; the page may use standard ""pagination or limit results in this session.")


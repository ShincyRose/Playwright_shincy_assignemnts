# from playwright.sync_api import sync_playwright


# def test_context_isolation():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)

#         # Create two independent browser contexts
#         context1 = browser.new_context()
#         context2 = browser.new_context()

#         page1 = context1.new_page()
#         page2 = context2.new_page()

#         page1.goto("https://www.google.com")
#         page2.goto("https://www.google.com")

#         # Store a cookie in the first context only
#         context1.add_cookies([
#             {
#                 "name": "session_test",
#                 "value": "context1",
#                 "url": "https://www.google.com"
#             }
#         ])

#         cookies1 = context1.cookies()
#         cookies2 = context2.cookies()

#         print("Context 1 cookies:", cookies1)
#         print("Context 2 cookies:", cookies2)

#         assert any(
#             cookie["name"] == "session_test"
#             for cookie in cookies1
#         )

#         assert not any(
#             cookie["name"] == "session_test"
#             for cookie in cookies2
#         )

#         context1.close()
#         context2.close()
#         browser.close()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Create a .env file and read BASE_URL
# import os
# from dotenv import load_dotenv
# from playwright.sync_api import Page


# load_dotenv()

# BASE_URL = os.getenv("BASE_URL")


# def test_open_base_url(page: Page):
#     assert BASE_URL is not None, "BASE_URL is missing in .env"

#     page.goto(BASE_URL)

#     print("Opened URL:", page.url)

#     assert page.url.startswith("https://")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Navigate, click an element, fill a field, and press Enter
from playwright.sync_api import Page, expect


def test_google_search(page: Page):
    page.goto("https://www.google.com")

    # Locate the search field
    search_box = page.locator("textarea[name='q']")

    # Fill in the search field
    search_box.fill("Playwright Python")

    # Press Enter
    search_box.press("Enter")

    # Verify that search results have loaded
    expect(page.locator("body")).to_contain_text(
        "Playwright"
    )

    print("Search completed successfully")

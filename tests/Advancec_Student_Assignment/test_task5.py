
import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def mock_product_api():
    return {
        "source_endpoint": "mock://trainer-api/products/B07JPX9CR7",
        "status_code": 200,
        "data": {
            "product_id": "B07JPX9CR7",
            "title": "Dell WM118 Wireless Mouse"
        }
    }


def normalize_text(value):
    """Normalize whitespace and case for comparison."""
    return " ".join(value.split()).casefold()


def test_amazon_ui_api_validation(page: Page, mock_product_api):

    api_response = mock_product_api
    api_data = api_response["data"]

    endpoint = api_response["source_endpoint"]

    print("========== MOCK API DETAILS ==========")
    print("Source endpoint:", endpoint)
    print("Status code:", api_response["status_code"])
    print("API field product_id:", api_data["product_id"])
    print("API field title:", api_data["title"])

    assert api_response["status_code"] == 200

    product_id = api_data["product_id"]

    product_url = (f"https://www.amazon.in/dp/{product_id}")

    page.goto(product_url,wait_until="domcontentloaded")

    ui_title_locator = page.locator("span#productTitle")

    expect(ui_title_locator).to_be_visible(timeout=20000)

    ui_title = " ".join(ui_title_locator.inner_text().split())

    print("========== UI DETAILS ==========")
    print("UI product title:", ui_title)
    print("UI product URL:", page.url)

    match = re.search(r"/dp/([A-Z0-9]{10})",page.url)

    assert match is not None, ("Could not extract a product identifier from the UI URL.")

    ui_product_id = match.group(1)

    print("UI field product_id:", ui_product_id)

    assert ui_product_id == api_data["product_id"], (f"Product ID mismatch!\n"f"Source endpoint: {endpoint}\n"f"API field: product_id = {api_data['product_id']}\n"f"UI field: product_id = {ui_product_id}")

    print("PASS: Product identifiers match.")

    api_title = api_data["title"]

    normalized_api_title = normalize_text(api_title)
    normalized_ui_title = normalize_text(ui_title)

    assert normalized_ui_title.startswith(normalized_api_title), (f"Product title mismatch!\n"f"Source endpoint: {endpoint}\n"f"API field: title = '{api_title}'\n"f"UI field: title = '{ui_title}'")

    print("PASS: UI title starts with the expected API title.")
    print("========== VALIDATION SUMMARY ==========")
    print("Endpoint:", endpoint)
    print("Fields validated: product_id, title")
    print("Result: All validations passed.")

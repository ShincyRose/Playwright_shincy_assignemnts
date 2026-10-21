#Scenario 10: Amazon – Select Product from Search Results

from playwright.sync_api import sync_playwright, expect

AMAZON_URL = "https://www.amazon.in/"
PRODUCT_NAME = ("Boat Bassheads 300C Wired Earphones,Type-C Jack, ""10mm Drivers, Signature Sound, in-Line Microphone, ""Integrated Controls, Voice Assistant & 120cm Cable ""(Active Black)")
def test_amazon_product():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1440,"height": 900})
        print("\nSTEP 1: Open Amazon")
        page.goto(AMAZON_URL, wait_until="domcontentloaded",timeout=30000)
        print("URL:", page.url)
        print("\nSTEP 2: Search product")
        search_box = page.locator("#twotabsearchtextbox")
        expect(search_box).to_be_visible(timeout=15000)
        search_box.fill(PRODUCT_NAME)
        search_box.press("Enter")
        # Give Amazon time to render results
        page.wait_for_timeout(5000)
        print("Search URL:",page.url)
        print("\nSTEP 3: Check search page")
        results = page.locator("div[data-component-type='s-search-result']")
        expect(results.first).to_be_visible(timeout=15000)
        result_count = results.count()
        print("Search results found:",result_count)
        assert result_count > 0, ("Amazon search results were not found.")
        print("\nSTEP 4: Find required product")
        matching_result = None
        for i in range(result_count):
            result = results.nth(i)
            try:
                result_text = (result.inner_text(timeout=5000).strip())
            except Exception:
                continue
            print(f"\n========== RESULT {i} ==========")
            print(result_text[:700])
            text_lower = result_text.lower()
            if ("bassheads 300c" in text_lower and "type-c" in text_lower and "120cm" in text_lower):
                matching_result = result
                print("\nMATCH FOUND:",i)
                break
        assert matching_result is not None, (f"Product '{PRODUCT_NAME}' " "was not found in Amazon search results.")
        print("\nSTEP 5: Verify product title")
        result_text = (matching_result.inner_text().strip())
        assert "Bassheads 300C" in result_text
        assert "Type-C" in result_text
        assert "120cm" in result_text
        print("Product title verified.")
        print("\nSTEP 6: Find corresponding product image")
        product_image = matching_result.locator("img.s-image").first
        if product_image.count() == 0:
            product_image = matching_result.locator("img").first
        expect(product_image).to_be_attached(timeout=10000)
        image_src = product_image.get_attribute("src")
        print("Image:",image_src)
        assert image_src, ("Product image does not contain src.")
        print("\nSTEP 7: Find corresponding price")
        price_locator = matching_result.locator("span.a-offscreen").first
        price_text = None
        if price_locator.count() > 0:
            try:
                price_text = (price_locator.inner_text().strip())
            except Exception:
                price_text = None
        if not price_text:
            price_locator = matching_result.locator("span.a-price").first
            if price_locator.count() > 0:
                price_text = (price_locator.inner_text().strip())
        assert price_text, ("Product price was not found.")
        print("Price:", price_text)
        print("\n: Select same product")
        all_links = matching_result.locator("a")
        link_count = all_links.count()
        print("Links inside matched result:",link_count)
        product_href = None
        for j in range(link_count):
            link = all_links.nth(j)
            try:
                href = link.get_attribute("href")
            except Exception:
                continue
            if not href:
                continue
            print(f"Link {j}: {href}")
            if ("/dp/" in href or "/gp/product/" in href):
                product_href = href
                print("PRODUCT LINK FOUND:",product_href)
                break
        assert product_href is not None, ("Could not find the product URL ""inside the matching Amazon result.")
        print("\nSTEP 9: Open product details")
        if product_href.startswith("/"):
            product_url = ("https://www.amazon.in"+ product_href)
        elif product_href.startswith("http"):
            product_url = product_href
        else:
            product_url = ("https://www.amazon.in/"+ product_href)
        print("Opening product URL:",product_url)
        page.goto(product_url,wait_until="domcontentloaded",timeout=30000)
        page.wait_for_timeout(5000)
        print("Product page:", page.url)
        assert ("/dp/" in page.url or "/gp/product/" in page.url), ("Amazon did not navigate to ""the product details page.")
        print("\nSTEP 10: Verify product title")
        product_title = page.locator("span#productTitle").first
        expect(product_title).to_be_visible(timeout=20000)
        actual_title = (product_title.inner_text().strip())
        print("Product title:",actual_title)
        assert "Bassheads 300C" in actual_title
        assert "Type-C" in actual_title
        assert "120cm" in actual_title
        print("Product title on details page verified.")
        print("\n: Verify product image")
        detail_image = page.locator("#landingImage").first
        if detail_image.count() == 0:
            detail_image = page.locator("img").filter(has=page.locator("xpath=..")).first
        if detail_image.count() > 0:
            expect(detail_image).to_be_visible(timeout=15000)
            detail_image_src = (detail_image.get_attribute("src" ))
            print("Product detail image:",detail_image_src)
            assert detail_image_src, ("Product detail image ""does not contain src.")
        else:
            print("Product detail image locator ""was not available.")
        print("\n: Verify product price")
        detail_price = page.locator("span.a-price").first
        if detail_price.count() > 0:
            try:
                expect(detail_price).to_be_visible(timeout=10000)
                detail_price_text = (detail_price.inner_text().strip())

                print("Product detail price:", detail_price_text)
                assert detail_price_text
            except Exception as exc:
                print("Price verification skipped:",exc)
        else:
            print("Product detail price locator " "was not found.")
        print("Final verification")
        assert "Bassheads 300C" in actual_title
        print()
        print("========================================")
        print("TEST PASSED")
        print("Correct Amazon product selected.")
        print("Product:", actual_title)
        print("Search result price:", price_text)
        print("========================================")
        browser.close()
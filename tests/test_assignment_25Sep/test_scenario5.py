#Scenario 5: DemoWebShop – Product Name and Rating
from playwright.sync_api import Page, expect
def test_product_rating_by_name(page: Page):
    page.goto("https://demowebshop.tricentis.com/")
    page.locator("//div[contains(@class,'listbox')]""//a[normalize-space()='Books']").click()
    product_name = "Computing and Internet"
    product = page.locator(f"//div[contains(@class,'product-item')]"f"[.//h2[contains(@class,'product-title')]/a"f"[normalize-space()='{product_name}']]")
    expect(product).to_be_visible()
    actual_product_name = product.locator("xpath=.//h2[contains(@class,'product-title')]/a").inner_text()
    rating_element = product.locator("xpath=.//div[contains(@class,'product-rating-box')]""//div[@class='rating']")
    expect(rating_element).to_be_visible()
    rating_width = rating_element.evaluate("(element) => parseFloat(getComputedStyle(element).width)")
    total_width = rating_element.locator("xpath=..").evaluate("(element) => parseFloat(getComputedStyle(element).width)")
    rating = round((rating_width / total_width) * 5,1)
    print("Product name:", actual_product_name)
    print("Product rating:", rating, "/ 5")
    assert actual_product_name == product_name
    assert rating_element.count() == 1
#Scenario 3: DemoWebShop – Select Product by Price
from playwright.sync_api import Page, expect
def test_add_product_by_price(page: Page):
    page.goto("https://demowebshop.tricentis.com/")
    page.locator("//a[normalize-space()='Books']").first.click() # Go to Books
    price = "10.00" # Price used to identify the product
    product = page.locator(f"(//div[contains(@class,'product-item')]" f"[.//span[contains(@class,'price') and normalize-space()='{price}']])[1]")
    expect(product).to_be_visible()
    product_name = product.locator("xpath=.//h2[contains(@class,'product-title')]/a").inner_text()
    print("Product name:", product_name)
    print("Product price:", price)
    add_to_cart = product.locator("xpath=.//input[@value='Add to cart']")
    expect(add_to_cart).to_be_visible()
    add_to_cart.click()
    cart_qty = page.locator("//span[contains(@class,'cart-qty')]")
    expect(cart_qty).to_have_text("(1)")
    print("Product added to cart")
    page.locator("//a[contains(@href,'cart')]").first.click()
    expect(page.locator("text=Your Shopping Cart is empty!")).not_to_be_visible()
    cart_product = page.locator(f"//a[contains(@class,'product-name') " f"and normalize-space()='{product_name}']")
    expect(cart_product).to_be_visible()
    print("Product successfully verified in cart:", product_name)

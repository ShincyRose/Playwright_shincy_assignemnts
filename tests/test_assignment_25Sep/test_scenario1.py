#Scenario 1: DemoWebShop – Product Name to Add to Cart
from playwright.sync_api import Page, expect
def test_add_book_to_cart(page: Page):
    page.goto("https://demowebshop.tricentis.com/")
    page.locator( "//a[@href='/books' and normalize-space()='Books']").first.click()
    product_name = "Computing and Internet"
    product = page.locator(f"//h2[@class='product-title']/a[normalize-space()='{product_name}']")
    product_container = product.locator("xpath=ancestor::div[contains(@class,'product-item')]")
    add_to_cart = product_container.locator("xpath=.//input[@value='Add to cart']")
    add_to_cart.click()
    expect(page.get_by_text("The product has been added to your shopping cart")).to_be_visible()
    page.locator("//a[@href='/cart']").first.click()
    cart_product = page.locator(f"//td[@class='product']/a[normalize-space()='{product_name}']")
    expect(cart_product).to_be_visible()
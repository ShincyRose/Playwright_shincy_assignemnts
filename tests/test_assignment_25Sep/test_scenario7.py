#Scenario 7: DemoWebShop – Multiple Products
from playwright.sync_api import Page, expect
def test_dynamic_product_add_to_cart(page: Page):
    page.goto("https://demowebshop.tricentis.com/", wait_until="domcontentloaded")
    page.locator("//div[contains(@class,'listbox')]""//a[normalize-space()='Books']").click()
    products = page.locator("div.product-item")
    expect(products.first).to_be_visible()
    product_count = products.count()
    assert product_count > 0, ("No products displayed in the category.")
    print("Number of products:", product_count)
    for product in products.all():
        name = product.locator("xpath=.//h2[contains(@class,'product-title')]/a")
        if name.count() == 0:
            continue
        product_name = name.inner_text().strip()
        print("Product name:", product_name)
    for product in products.all():
        name = product.locator("xpath=.//h2[contains(@class,'product-title')]/a")
        if name.count() == 0:
            continue
        product_name = name.inner_text().strip()
        add_to_cart = product.locator("xpath=.//input[""@value='Add to cart' ""or contains(@class,'product-box-add-to-cart')""]")
        if add_to_cart.count() > 0:
            print(f"Add to Cart found for: {product_name}")
        else:
            print(f"Add to Cart not available for: {product_name}")
    selected_product = None
    for product in products.all():
        name = product.locator("xpath=.//h2[contains(@class,'product-title')]/a")
        if name.count() == 0:
            continue
        add_to_cart = product.locator("xpath=.//input[""@value='Add to cart' ""or contains(@class,'product-box-add-to-cart')""]")

        if add_to_cart.count() > 0:
            selected_product = product
            break
    assert selected_product is not None, ("No displayed product has an Add to Cart button.")
    selected_name = selected_product.locator("xpath=.//h2[contains(@class,'product-title')]/a").inner_text().strip()
    print("Dynamically selected product:",selected_name)
    selected_add_to_cart = selected_product.locator("xpath=.//input[""@value='Add to cart' ""or contains(@class,'product-box-add-to-cart')""]")
    expect(selected_add_to_cart).to_be_visible()
    selected_add_to_cart.click()
    cart_quantity = page.locator("span.cart-qty")
    expect(cart_quantity).to_have_text("(1)")
    print(f"'{selected_name}' was successfully ""added to the cart.")
from playwright.sync_api import sync_playwright, expect
import random
import string

PARABANK_URL = ("https://parabank.parasoft.com/parabank/index.htm")

def generate_user():

    suffix = (str(random.randint(10000, 99999)))
    return {
        "username": "testuser" + suffix,
        "password": "Test@12345",
        "first_name": "Test",
        "last_name": "User",
        "address": "123 Test Street",
        "city": "Kochi",
        "state": "Kerala",
        "zip_code": "682001",
        "phone": "9876543210",
        "ssn": "123456789",
    }

def test_parabank_transfer_funds():

    user = generate_user()
    username = user["username"]
    password = user["password"]
    transfer_amount = "10"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1440,"height": 900})

        print("\nSTEP 1: Open ParaBank")

        page.goto(PARABANK_URL,wait_until="domcontentloaded",timeout=30000)

        print("URL:",page.url)

        expect(page.locator("body")).to_contain_text("ParaBank",timeout=15000)

        print("Register new customer")

        register_link = page.get_by_role("link",name="Register")
        expect(register_link).to_be_visible(timeout=15000)
        register_link.click()
        page.wait_for_load_state("domcontentloaded",timeout=30000)

        page.wait_for_timeout(1000)

        print("Register URL:",page.url)

        expect(page.locator("body")).to_contain_text("Signing up is easy",timeout=15000)

        print("Enter customer details")

        page.locator("#customer\\.firstName").fill(user["first_name"])

        page.locator("#customer\\.lastName").fill(user["last_name"])

        page.locator("#customer\\.address\\.street").fill(user["address"])

        page.locator("#customer\\.address\\.city").fill(user["city"])

        page.locator("#customer\\.address\\.state").fill(user["state"])

        page.locator("#customer\\.address\\.zipCode").fill(user["zip_code"])

        page.locator("#customer\\.phoneNumber").fill(user["phone"])

        page.locator("#customer\\.ssn").fill(user["ssn"])

        page.locator("#customer\\.username").fill(username)

        page.locator("#customer\\.password").fill(password)

        page.locator("#repeatedPassword").fill(password)

        print("Username:",username)

        print("\nSTEP 4: Submit registration" )
        register_button = page.get_by_role("button",name="Register")
        expect(register_button).to_be_visible(timeout=15000)
        register_button.click()
        page.wait_for_load_state("domcontentloaded",timeout=30000)

        page.wait_for_timeout(1500)

        print("Registration URL:",page.url)
        print("Verify registration")
        body_text = page.locator("body").inner_text()
        print(body_text[:2500])
        expect(page.locator("body")).to_contain_text("Welcome",timeout=15000)
        print("Registration successful.")

        print("Verify logged-in state")

        expect(page.get_by_role("link",name="Accounts Overview")).to_be_visible(timeout=15000)

        print("User is logged in.")

        print("Navigate to Accounts Overview")

        page.get_by_role("link",name="Accounts Overview").click()

        page.wait_for_load_state("domcontentloaded",timeout=30000)

        page.wait_for_timeout(1000)

        print("Accounts Overview URL:",page.url)

        expect(page.locator("body")).to_contain_text("Accounts Overview",timeout=15000)

        print("Identify accounts")

        account_links = page.locator("table#accountTable tbody tr td a")

        account_count = account_links.count()

        print("Accounts found:",account_count)
        if account_count < 2:

            print("Only one account exists.")

            print("Creating a second account...")

            page.get_by_role("link",name="Open New Account").click()

            page.wait_for_load_state("domcontentloaded",timeout=30000)

            page.wait_for_timeout(1000)

            print("Open New Account URL:",page.url)

            expect(page.locator("body")).to_contain_text("Open New Account",timeout=15000)

            account_type = page.locator("#type")

            expect(account_type).to_be_visible(timeout=15000)

            account_type.select_option("SAVINGS")

            from_account_selector = page.locator("#fromAccountId")

            expect(from_account_selector).to_be_visible(timeout=15000)

            existing_account = (page.locator("#fromAccountId option").first.get_attribute("value"))

            assert existing_account

            from_account_selector.select_option(existing_account)

            open_account_button = page.get_by_role("button",name="Open New Account")

            expect(open_account_button).to_be_visible(timeout=15000)

            open_account_button.click()

            page.wait_for_load_state("domcontentloaded",timeout=30000)

            page.wait_for_timeout(1500)

            print("New account created.")

            page.get_by_role("link",name="Accounts Overview").click()

            page.wait_for_load_state("domcontentloaded",timeout=30000)

            page.wait_for_timeout(1000)

            account_links = page.locator("table#accountTable tbody tr td a")

            account_count = account_links.count()

            print("Accounts after creation:",account_count)

        print("Verify two accounts")

        assert account_count >= 2, ("At least two accounts are required ""for a transfer.")

        from_account = (account_links.nth(0).inner_text().strip())

        to_account = (account_links.nth(1).inner_text().strip())

        print("From Account:",from_account)

        print("To Account:",to_account)

        assert from_account
        assert to_account

        assert from_account != to_account
     
        print(" Navigate to Transfer Funds")

        page.get_by_role("link",name="Transfer Funds").click()

        page.wait_for_load_state("domcontentloaded",timeout=30000)

        page.wait_for_timeout(1000)

        print("Transfer URL:",page.url)

        expect(page.locator("body")).to_contain_text("Transfer Funds",timeout=15000)
        print("Enter transfer amount")

        amount_field = page.locator("#amount")

        expect(amount_field).to_be_visible(timeout=15000)

        amount_field.fill(transfer_amount)

        print("Transfer amount:",amount_field.input_value())

        print("Select From Account")

        from_dropdown = page.locator( "#fromAccountId")

        expect(from_dropdown).to_be_visible(timeout=15000)

        from_dropdown.select_option(label=from_account)

        print("From account selected:",from_dropdown.input_value())
        print(" Select To Account")

        to_dropdown = page.locator("#toAccountId")

        expect(to_dropdown).to_be_visible(timeout=15000)

        to_dropdown.select_option(label=to_account)

        print("To account selected:",to_dropdown.input_value())

        assert (from_dropdown.input_value()!= to_dropdown.input_value())

        print("Transfer funds")

        transfer_button = page.get_by_role("button",name="Transfer")

        expect(transfer_button).to_be_visible(timeout=15000)

        transfer_button.click()

        page.wait_for_load_state("domcontentloaded",timeout=30000)

        page.wait_for_timeout(1500)

        print("Transfer result URL:",page.url)
        print("Verify transfer confirmation")

        result_text = page.locator("body").inner_text()

        print(result_text[:3000])

        expect(page.locator("body")).to_contain_text("Transfer Complete",timeout=15000)

        print("Transfer confirmation verified.")

        print("Navigate to Accounts Overview")

        page.get_by_role("link",name="Accounts Overview").click()

        page.wait_for_load_state("domcontentloaded",timeout=30000)

        page.wait_for_timeout(1000)

        print("Accounts Overview URL:",page.url)

        print("Open destination account")

        destination_account = (page.locator("table#accountTable tbody tr td a").filter(has_text=to_account).first)

        expect(destination_account).to_be_visible(timeout=15000)

        destination_account.click()

        page.wait_for_load_state("domcontentloaded",timeout=30000)

        page.wait_for_timeout(1000)

        print("Account details URL:",page.url)

        print("Verify transaction history")

        account_body = page.locator("body")

        account_text = account_body.inner_text()

        print("Account details:")

        print(account_text[:4000])

        assert ("Transaction" in account_text or "transaction" in account_text), ("Transaction history was not displayed.")

        amount_found = ("$10.00" in account_text or "$10" in account_text)

        assert amount_found, ("Transferred amount was not found ""in transaction history.")

        print("Transferred amount verified " "in transaction history." )

        print("Logout")

        logout_link = page.get_by_role( "link",name="Log Out")

        expect(logout_link).to_be_visible(timeout=15000)

        logout_link.click()

        page.wait_for_load_state("domcontentloaded",timeout=30000)

        page.wait_for_timeout(1000)

        print("Logout URL:",page.url)

        expect(page.locator("input[name='username']")).to_be_visible(timeout=15000)

        print("=============================================")

        print("TEST PASSED")

        print("==============================================")

        print("Username:", username)

        print("From Account:",from_account)

        print("To Account:",to_account)

        print("Transfer Amount:","$" + transfer_amount + ".00")

        print("Transfer completed successfully.")

        print("Transaction history verified.")

        print("User logged out successfully.")

        print("==============================================")

        browser.close()
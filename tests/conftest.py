
from pathlib import Path
import pytest

PROJECT_DIR = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = PROJECT_DIR / "test-results" / "screenshots"


@pytest.fixture
def auth_state_path():
    return PROJECT_DIR / "playwright" / ".auth" / "user.json"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page is not None and not page.is_closed():
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            screenshot_path = SCREENSHOT_DIR / f"{item.name}.png"

            try:
                page.screenshot(
                    path=str(screenshot_path),
                    full_page=True
                )
                print(f"\nFailure screenshot: {screenshot_path}")
            except Exception as error:
                print(f"\nScreenshot could not be captured: {error}")

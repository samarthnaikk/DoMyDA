from playwright.async_api import async_playwright

async def open_browser():
    """Launch Playwright Chromium browser and return (playwright, browser, context, page).

    The caller is responsible for closing the returned objects (context.close(), browser.close(), playwright.stop()).
    """
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context(accept_downloads=True)
    page = await context.new_page()
    return p, browser, context, page

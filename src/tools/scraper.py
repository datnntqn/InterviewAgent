from playwright.sync_api import sync_playwright


class WebsiteScraper:
    """
    Simple Playwright-based scraper tool.
    Used by CrewAI agents to fetch raw text from a webpage.
    """

    def scrape_text(self, url: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            content = page.inner_text("body")
            browser.close()
        return content

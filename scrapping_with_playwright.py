import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def myscrapping():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # ---------------------
        # LOGIN
        # ---------------------
        page.goto("https://app.airwork.ai/login")

        page.fill("input[name='email']", EMAIL)
        page.fill("input[name='password']", PASSWORD)

        page.click("button[type='submit']")

        page.wait_for_timeout(5000)
        print("Login Successful")

        # ---------------------
        # COLLECT JOB LINKS
        # ---------------------

        job_elements = page.locator(
            "xpath=/html/body/div[2]/div/div/main/div/div/div/div[2]//a"
        )

        job_links = []

        for i in range(job_elements.count()):
            link = job_elements.nth(i).get_attribute("href")
            if link:
                job_links.append(link)

        print(f"Job links: {job_links}")
        print("Total jobs found:", len(job_links))

        # ---------------------
        # VISIT EACH JOB
        # ---------------------
        for link in job_links:

            full_url = (
                "https://app.airwork.ai" + link
                if link.startswith("/")
                else link
            )

            print("Opening:", full_url)

            page.goto(full_url)
            page.wait_for_timeout(1500)

            # ------------------ ID based ------------------
            try:
                summary = page.locator("#job-summary").inner_text()
            except:
                summary = ""

            try:
                description = page.locator("#job-description").inner_text()
            except:
                description = ""

            # ------------------ UI based ------------------
            try:
                catchphrase = page.locator(
                    "div.flex.flex-1.flex-col.gap-0\\.5 p"
                ).inner_text()
            except:
                catchphrase = ""

            try:
                title = page.locator(
                    "div.flex.flex-1.flex-col.gap-0\\.5 h1"
                ).inner_text()
            except:
                title = ""

            try:
                salary = page.locator(
                    "//span[text()='Salary range']/following::span[1]"
                ).inner_text()
            except:
                salary = ""

            try:
                job_type = page.locator(
                    "//span[text()='Type']/following::span[1]"
                ).inner_text()
            except:
                job_type = ""

            try:
                job_nature = page.locator(
                    "//span[text()='Nature']/following::span[1]"
                ).inner_text()
            except:
                job_nature = ""

            print("Catchphrase:", catchphrase)
            print("Title:", title)
            print("Salary:", salary)
            print("Type:", job_type)
            print("Nature:", job_nature)
            print("Summary:", summary)
            print("----------------------")

        browser.close()


if __name__ == "__main__":
    myscrapping()
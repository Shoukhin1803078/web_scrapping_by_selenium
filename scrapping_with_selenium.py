from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
import dotenv

dotenv.load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def myscrapping():

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # ✅ Headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # ---------------- LOGIN ----------------
    driver.get("https://app.airwork.ai/login")
    time.sleep(3)

    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(5)
    print("Login Successful")

    # ---------------- JOB LINKS ----------------
    job_elements = driver.find_elements(
        By.XPATH,
        "/html/body/div[2]/div/div/main/div/div/div/div[2]//a"
    )

    job_links = [job.get_attribute("href") for job in job_elements if job.get_attribute("href")]

    print(f"Total jobs found: {len(job_links)}")

    # ---------------- VISIT JOBS ----------------
    for link in job_links:

        driver.get("https://app.airwork.ai" + link if link.startswith("/") else link)
        time.sleep(2)

        def safe_find(by, value):
            try:
                return driver.find_element(by, value).text
            except:
                return ""

        summary = safe_find(By.ID, "job-summary")
        description = safe_find(By.ID, "job-description")
        catchphrase = safe_find(By.CSS_SELECTOR, "div.flex.flex-1.flex-col.gap-0\\.5 p")
        title = safe_find(By.CSS_SELECTOR, "div.flex.flex-1.flex-col.gap-0\\.5 h1")
        salary = safe_find(By.XPATH, "//span[text()='Salary range']/following::span[1]")
        job_type = safe_find(By.XPATH, "//span[text()='Type']/following::span[1]")
        job_nature = safe_find(By.XPATH, "//span[text()='Nature']/following::span[1]")

        print(title, salary, job_type, job_nature)
        print("----------------------")

    driver.quit()


if __name__ == "__main__":
    myscrapping()
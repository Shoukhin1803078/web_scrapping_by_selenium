from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os 
import dotenv

dotenv.load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()

# ---------------------
# LOGIN
# ---------------------

driver.get("https://app.airwork.ai/login")

time.sleep(3)

driver.find_element(By.NAME, "email").send_keys(EMAIL)
driver.find_element(By.NAME, "password").send_keys(PASSWORD)

driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

time.sleep(5)

print("Login Successful")

# ---------------------
# COLLECT JOB LINKS
# ---------------------

job_elements = driver.find_elements(
    By.XPATH,
    "/html/body/div[2]/div/div/main/div/div/div/div[2]//a"
)

job_links = []

for job in job_elements:
    link = job.get_attribute("href")

    if link:   # None হলে skip
        job_links.append(link)

print(f"Job links: {job_links}")


print("Total jobs found:", len(job_links))

# ---------------------
# VISIT EACH JOB
# ---------------------

for link in job_links:

    print("Opening:", link)

    driver.get("https://app.airwork.ai" + link if link.startswith("/") else link)

    time.sleep(1)

# ---------------------------- By ID -----------------------------------
    try:
        summary = driver.find_element(
            By.ID,
            "job-summary"
        ).text
    except:
        summary = ""

    try:
        description = driver.find_element(
            By.ID,
            "job-description"
        ).text
    except:
        description = ""
# ---------------------------- By Others specific area -----------------------------------


    # Catchphrase
    try:
        catchphrase = driver.find_element(
            By.CSS_SELECTOR,
            "div.flex.flex-1.flex-col.gap-0\\.5 p"
        ).text
    except:
        catchphrase = ""

    # Job title
    try:
        title = driver.find_element(
            By.CSS_SELECTOR,
            "div.flex.flex-1.flex-col.gap-0\\.5 h1"
        ).text
    except:
        title = ""

    # Salary
    try:
        salary = driver.find_element(
            By.XPATH,
            "//span[text()='Salary range']/following::span[1]"
        ).text
    except:
        salary = ""
    
    try:
        job_type = driver.find_element(
            By.XPATH,
            "//span[text()='Type']/following::span[1]"
        ).text
    except:
        job_type = ""

    try:
        job_nature = driver.find_element(
            By.XPATH,
            "//span[text()='Nature']/following::span[1]"
        ).text
    except:
        job_nature = ""

    print("Catchphrase:", catchphrase)
    print("Title:", title)
    print("Salary:", salary)
    print("Type:", job_type)
    print("Nature:", job_nature)
    print("Summary:", summary)
    print("Description:", description)
    print("----------------------")


driver.quit()
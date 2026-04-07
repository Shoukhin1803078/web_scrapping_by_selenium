# web_scrapping_by_selenium
---
My prompt:
```
i want to do jobs scrapping from https://app.airwork.ai this website. 
so first i need to login here :
https://app.airwork.ai/login
For this login page after inspect this page i found this information:
- there is a Email address field with this id="_r_6t_-form-item" type="email" value="" name="email" 
- there is a password field with placeholder="Enter password" type="password" value="" name="password">
- there is a Login button with type="submit">Login</button>

Now after login I see 10 jobs card per page (paginated) :
In this class I see the Next button for moving to the next pages. 
<span class="hidden sm:block">Next</span> 

Now for page-1:
- In this class="flex flex-col gap-8" there are so many(10) anchor tag which represent  job cards.  

Now if i want to get the information of each jobs then i need to hit Apply button for each job cards
I see the Apply button is inside this class <span class="min-w-[55px] text-center">Apply</span>
or here i give the whole button Xpath  is /html/body/div[2]/div/div/main/div/div/div/div[2]/div/a[8]/div/div/div[1]/div[2]/button[2]

Now after hitting the Apply button for a job :

Headline:
catchphrase & Headline: In this class <div class="flex flex-1 flex-col gap-0.5"> there are two tags <p> and <h1>  Here from <p> tag we can get the catchphrase and from <h1> tag we can get the job_title
<div class="flex flex-1 flex-col gap-0.5"><p class="text-sm font-medium text-gray-500">Synesis IT PLC<!-- --> is hiring</p><h1 class="text-lg font-semibold wrap-break-word text-gray-900 md:text-2xl">Senior Mobile App Developer (React Native)</h1></div>

Summary & description div:
<div class="flex flex-1 flex-col gap-6"> in this class it consist of summary and description section. 
now inside this class there is a section with job-summary id 
<section aria-labelledby="job-summary-summary-heading" id="job-summary"> 

Now inside this Xpath : //*[@id="job-summary"]/div/div there is a class called <div data-slot="card-content" class="p-5"> 

Now inside this Xpath //*[@id="job-summary"]/div/div/div/div[6]/div[2] there is Salary range <div class="flex flex-col gap-1"><span class="text-sm font-semibold text-gray-500">Salary range</span><span class="text-sm font-medium text-gray-700">৳100000 - ৳120000 /mo (Negotiable)</span></div>

I need these informations . Now my question is Is my given prompt is correct to openai to give generate scrapping code or should i focus to give Xpath or class name or id or tags? 
```

---


OPENAI ANSWER:

তোমার observation খারাপ না 👍 তুমি ভালোভাবে inspect করে অনেক element বের করেছো। কিন্তু OpenAI বা কোনো developer-কে scraping code generate করতে দিলে prompt একটু অন্যভাবে দিলে বেশি reliable code পাওয়া যায়।
কারণ scraping-এ XPath দিলে code খুব fragile হয়ে যায় (page একটু change হলেই ভেঙে যায়)। তাই priority সাধারণত এমন হয়:

Best selector priority (scraping এ):

- 1️⃣ id → সবচেয়ে stable
- 2️⃣ name / data-attribute
- 3️⃣ class name (specific)
- 4️⃣ CSS selector
- 5️⃣ XPath (last option)

## 1️⃣ Login page এর জন্য তুমি যেভাবে দাও

তোমার prompt এ login info এভাবে দিলে ভালো হয়।
Example:
```
Website: https://app.airwork.ai/login

Login fields:
Email field:
input[name="email"]
type=email

Password field:
input[name="password"]
type=password

Login button:
button[type="submit"]
text = Login
```
👉 এখানে XPath দরকার নাই।


---

# 2️⃣ Job cards extraction prompt কেমন হওয়া উচিত

তুমি লিখতে পারো:

```
After login redirect to job listing page.

Each page contains 10 job cards.

Job cards container:
div.flex.flex-col.gap-8

Each job card is inside an anchor tag <a>.

For each job card click the Apply button.

Apply button text:
Apply

Pagination:
Next button text = "Next"
```

---

# 3️⃣ Job details extraction

এখানে XPath না দিয়ে structure বললে ভালো।

Example:

```
After clicking Apply button a job details page opens.

Catchphrase:
div.flex.flex-1.flex-col.gap-0.5 > p

Job title:
div.flex.flex-1.flex-col.gap-0.5 > h1

Job summary section:
section#job-summary

Salary range:
inside job-summary card content
label text = "Salary range"
value inside span.text-gray-700
```

---

# 4️⃣ XPath কেন avoid করা ভালো

তুমি যে XPath দিয়েছো:

```
/html/body/div[2]/div/div/main/div/div/div/div[2]/div/a[8]/div/div/div[1]/div[2]/button[2]
```

এইটা **খুব brittle**।

যদি page এ নতুন div add হয় → XPath ভেঙে যাবে।

---

# 5️⃣ Scraping করার best approach (এই site এর জন্য)

এই ধরনের **login + pagination site** scrape করতে usually ব্যবহার করা হয়:

**Selenium / Playwright**

Python example structure:

```
1 login
2 wait for jobs page
3 loop pages
4 collect job cards
5 click apply
6 scrape details
7 go back
8 next page
```

---

# 6️⃣ Real pro tip (সবচেয়ে important)

Inspect করলে অনেক সময় **API call থাকে**।

Airwork site এ খুব সম্ভবত jobs API দিয়ে load হয়।

Network tab → XHR / Fetch check করো।

যদি এমন কিছু পাও:

```
/api/jobs
```

তাহলে scraping না করে **direct API hit করাই best**।

---

# 7️⃣ তোমার prompt আরও powerful করতে চাইলে

এভাবে লিখো:

```
Generate Python Playwright scraping code for this site.

Requirements:

1. Login using email and password
2. Navigate to jobs listing page
3. Each page contains 10 jobs
4. Click Apply button for each job
5. Extract:

- Catchphrase
- Job title
- Salary range
- Summary

6. Go to next page using "Next" button
7. Repeat until no more pages
8. Save results to CSV
```

---

# 🔥 তোমাকে একটা important question

তুমি কি **Network tab check করেছো?**

মানে:

```
Inspect
→ Network
→ XHR / Fetch
→ page reload
```

যদি API থাকে তাহলে scraping **১০ গুণ সহজ হয়ে যাবে**।

---

চাও হলে তুমি আমাকে এই ৩টা screenshot বা info দাও:

1️⃣ **Network → XHR list**

2️⃣ **Job list request URL**

3️⃣ **Response JSON**



# ok now based on my giving prompt give me easy code for scrapping till that portion that i give good input

তুমি যেহেতু **login → job list → Apply → job details** পর্যন্ত scrape করতে চাও, এই ধরনের dynamic site-এ **Playwright** ব্যবহার করা সবচেয়ে সহজ এবং stable।

আমি তোমার দেওয়া structure অনুযায়ী একটা **simple Python scraping script** দিচ্ছি।

⚠️ Note

- এটা **educational example**
- তোমাকে নিজের **email/password** দিতে হবে
- page structure change হলে selector update লাগতে পারে

---

# 1️⃣ First install Playwright

```
pip install playwright
playwright install
```

---

# 2️⃣ Simple Scraping Code

```
fromplaywright.sync_apiimportsync_playwright
importtime

EMAIL="your_email_here"
PASSWORD="your_password_here"

defscrape_airwork():

withsync_playwright()asp:

browser=p.chromium.launch(headless=False)
page=browser.new_page()

# -----------------------------
# 1. Login
# -----------------------------
page.goto("https://app.airwork.ai/login")

page.fill('input[name="email"]',EMAIL)
page.fill('input[name="password"]',PASSWORD)

page.click('button[type="submit"]')

page.wait_for_load_state("networkidle")

print("Login successful")

# -----------------------------
# 2. Collect job cards
# -----------------------------
job_cards=page.query_selector_all("div.flex.flex-col.gap-8 a")

print(f"Found{len(job_cards)} jobs")

foriinrange(len(job_cards)):

job_cards=page.query_selector_all("div.flex.flex-col.gap-8 a")
job=job_cards[i]

print(f"Opening job{i+1}")

job.click()

page.wait_for_load_state("networkidle")

# -----------------------------
# 3. Click Apply button
# -----------------------------
try:
page.click('text=Apply')
except:
pass

page.wait_for_timeout(2000)

# -----------------------------
# 4. Extract information
# -----------------------------
try:
catchphrase=page.inner_text(
"div.flex.flex-1.flex-col.gap-0\\.5 p"
                )
except:
catchphrase=""

try:
title=page.inner_text(
"div.flex.flex-1.flex-col.gap-0\\.5 h1"
                )
except:
title=""

try:
salary=page.inner_text(
"text=Salary range >> xpath=.. >> span.text-gray-700"
                )
except:
salary=""

print("Catchphrase:",catchphrase)
print("Title:",title)
print("Salary:",salary)
print("------------------------")

page.go_back()
page.wait_for_load_state("networkidle")

browser.close()

scrape_airwork()
```

---

# 3️⃣ Code কী করছে

এই script step by step:

1️⃣ login page open

2️⃣ email/password fill

3️⃣ login click

4️⃣ job cards collect

5️⃣ প্রতিটা job open

6️⃣ **Apply button click**

7️⃣ scrape

- catchphrase
- job title
- salary

---

# 4️⃣ Next step (তোমার project এর জন্য)

পরের ধাপে তোমার দরকার হবে:

✔ pagination scrape

✔ description scrape

✔ summary scrape

✔ CSV save

✔ 1000+ jobs collect

---

💡 চাইলে আমি তোমাকে next message এ দেখাতে পারি:

**Airwork job scraper pro version**

যেখানে থাকবে:

- auto pagination
- 1000 jobs scrape
- CSV export
- error handling

এটা সাধারণত **40-50 lines code** এ হয়ে যাবে।

give me this for selenium code

ঠিক আছে 👍 তুমি যদি **Selenium** ব্যবহার করতে চাও তাহলে তোমার দেওয়া structure অনুযায়ী একটা **simple beginner-friendly scraping code** নিচে দিলাম।

এই code করবে:

1️⃣ login করবে

2️⃣ job cards collect করবে

3️⃣ প্রতিটা job open করবে

4️⃣ Apply button click করবে

5️⃣ catchphrase, job title, salary scrape করবে

---

# 1️⃣ Install packages

```
pip install selenium webdriver-manager
```

---

# 2️⃣ Selenium Scraper Code

```
fromseleniumimportwebdriver
fromselenium.webdriver.common.byimportBy
fromselenium.webdriver.common.keysimportKeys
fromselenium.webdriver.chrome.serviceimportService
fromwebdriver_manager.chromeimportChromeDriverManager

importtime

EMAIL="your_email"
PASSWORD="your_password"

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()

# -----------------------------
# 1 Login
# -----------------------------
driver.get("https://app.airwork.ai/login")

time.sleep(3)

driver.find_element(By.NAME,"email").send_keys(EMAIL)
driver.find_element(By.NAME,"password").send_keys(PASSWORD)

driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()

time.sleep(5)

print("Login Successful")

# -----------------------------
# 2 Collect job cards
# -----------------------------
jobs=driver.find_elements(By.CSS_SELECTOR,"div.flex.flex-col.gap-8 a")

print("Total jobs found:",len(jobs))

foriinrange(len(jobs)):

jobs=driver.find_elements(By.CSS_SELECTOR,"div.flex.flex-col.gap-8 a")

print(f"Opening job{i+1}")

jobs[i].click()

time.sleep(3)

# -----------------------------
# Click Apply
# -----------------------------
try:
apply_btn=driver.find_element(By.XPATH,"//span[text()='Apply']")
apply_btn.click()
time.sleep(2)
except:
print("Apply button not found")

# -----------------------------
# Extract Data
# -----------------------------
try:
catchphrase=driver.find_element(
By.CSS_SELECTOR,
"div.flex.flex-1.flex-col.gap-0\\.5 p"
        ).text
except:
catchphrase=""

try:
title=driver.find_element(
By.CSS_SELECTOR,
"div.flex.flex-1.flex-col.gap-0\\.5 h1"
        ).text
except:
title=""

try:
salary=driver.find_element(
By.XPATH,
"//span[text()='Salary range']/following::span[1]"
        ).text
except:
salary=""

print("Catchphrase:",catchphrase)
print("Title:",title)
print("Salary:",salary)
print("-----------------------")

driver.back()

time.sleep(3)

driver.quit()
```

---

# 3️⃣ Code flow (simple explanation)

এই script basically:

```
login
   ↓
collect 10 job cards
   ↓
open job
   ↓
click apply
   ↓
scrape info
   ↓
go back
   ↓
next job
```

---

# 4️⃣ Important thing

তোমার দেওয়া selector এর মধ্যে এইটা escape করা হয়েছে:

```
gap-0\.5
```

কারণ **`.` CSS selector এ special character**।

---

# 5️⃣ Next improvement (recommended)

তুমি next step এ add করতে পারো:

✔ pagination (Next button click)

✔ description scraping

✔ CSV save

✔ error handling

✔ WebDriverWait (time.sleep বাদ)




তুমি যেহেতু **login → job list → Apply → job details** পর্যন্ত scrape করতে চাও, এই ধরনের dynamic site-এ **Playwright** ব্যবহার করা সবচেয়ে সহজ এবং stable।

আমি তোমার দেওয়া structure অনুযায়ী একটা **simple Python scraping script** দিচ্ছি।

⚠️ Note

- এটা **educational example**
- তোমাকে নিজের **email/password** দিতে হবে
- page structure change হলে selector update লাগতে পারে

---

# 1️⃣ First install Playwright

```
pip install playwright
playwright install
```

---

# 2️⃣ Simple Scraping Code

```
fromplaywright.sync_apiimportsync_playwright
importtime

EMAIL="your_email_here"
PASSWORD="your_password_here"

defscrape_airwork():

withsync_playwright()asp:

browser=p.chromium.launch(headless=False)
page=browser.new_page()

# -----------------------------
# 1. Login
# -----------------------------
page.goto("https://app.airwork.ai/login")

page.fill('input[name="email"]',EMAIL)
page.fill('input[name="password"]',PASSWORD)

page.click('button[type="submit"]')

page.wait_for_load_state("networkidle")

print("Login successful")

# -----------------------------
# 2. Collect job cards
# -----------------------------
job_cards=page.query_selector_all("div.flex.flex-col.gap-8 a")

print(f"Found{len(job_cards)} jobs")

foriinrange(len(job_cards)):

job_cards=page.query_selector_all("div.flex.flex-col.gap-8 a")
job=job_cards[i]

print(f"Opening job{i+1}")

job.click()

page.wait_for_load_state("networkidle")

# -----------------------------
# 3. Click Apply button
# -----------------------------
try:
page.click('text=Apply')
except:
pass

page.wait_for_timeout(2000)

# -----------------------------
# 4. Extract information
# -----------------------------
try:
catchphrase=page.inner_text(
"div.flex.flex-1.flex-col.gap-0\\.5 p"
                )
except:
catchphrase=""

try:
title=page.inner_text(
"div.flex.flex-1.flex-col.gap-0\\.5 h1"
                )
except:
title=""

try:
salary=page.inner_text(
"text=Salary range >> xpath=.. >> span.text-gray-700"
                )
except:
salary=""

print("Catchphrase:",catchphrase)
print("Title:",title)
print("Salary:",salary)
print("------------------------")

page.go_back()
page.wait_for_load_state("networkidle")

browser.close()

scrape_airwork()
```

---

# 3️⃣ Code কী করছে

এই script step by step:

1️⃣ login page open

2️⃣ email/password fill

3️⃣ login click

4️⃣ job cards collect

5️⃣ প্রতিটা job open

6️⃣ **Apply button click**

7️⃣ scrape

- catchphrase
- job title
- salary

---

# 4️⃣ Next step (তোমার project এর জন্য)

পরের ধাপে তোমার দরকার হবে:

✔ pagination scrape

✔ description scrape

✔ summary scrape

✔ CSV save

✔ 1000+ jobs collect

---

💡 চাইলে আমি তোমাকে next message এ দেখাতে পারি:

**Airwork job scraper pro version**

যেখানে থাকবে:

- auto pagination
- 1000 jobs scrape
- CSV export
- error handling

এটা সাধারণত **40-50 lines code** এ হয়ে যাবে।

give me this for selenium code

ঠিক আছে 👍 তুমি যদি **Selenium** ব্যবহার করতে চাও তাহলে তোমার দেওয়া structure অনুযায়ী একটা **simple beginner-friendly scraping code** নিচে দিলাম।

এই code করবে:

1️⃣ login করবে

2️⃣ job cards collect করবে

3️⃣ প্রতিটা job open করবে

4️⃣ Apply button click করবে

5️⃣ catchphrase, job title, salary scrape করবে

---

# 1️⃣ Install packages

```
pip install selenium webdriver-manager
```

---

# 2️⃣ Selenium Scraper Code

```
fromseleniumimportwebdriver
fromselenium.webdriver.common.byimportBy
fromselenium.webdriver.common.keysimportKeys
fromselenium.webdriver.chrome.serviceimportService
fromwebdriver_manager.chromeimportChromeDriverManager

importtime

EMAIL="your_email"
PASSWORD="your_password"

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()

# -----------------------------
# 1 Login
# -----------------------------
driver.get("https://app.airwork.ai/login")

time.sleep(3)

driver.find_element(By.NAME,"email").send_keys(EMAIL)
driver.find_element(By.NAME,"password").send_keys(PASSWORD)

driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()

time.sleep(5)

print("Login Successful")

# -----------------------------
# 2 Collect job cards
# -----------------------------
jobs=driver.find_elements(By.CSS_SELECTOR,"div.flex.flex-col.gap-8 a")

print("Total jobs found:",len(jobs))

foriinrange(len(jobs)):

jobs=driver.find_elements(By.CSS_SELECTOR,"div.flex.flex-col.gap-8 a")

print(f"Opening job{i+1}")

jobs[i].click()

time.sleep(3)

# -----------------------------
# Click Apply
# -----------------------------
try:
apply_btn=driver.find_element(By.XPATH,"//span[text()='Apply']")
apply_btn.click()
time.sleep(2)
except:
print("Apply button not found")

# -----------------------------
# Extract Data
# -----------------------------
try:
catchphrase=driver.find_element(
By.CSS_SELECTOR,
"div.flex.flex-1.flex-col.gap-0\\.5 p"
        ).text
except:
catchphrase=""

try:
title=driver.find_element(
By.CSS_SELECTOR,
"div.flex.flex-1.flex-col.gap-0\\.5 h1"
        ).text
except:
title=""

try:
salary=driver.find_element(
By.XPATH,
"//span[text()='Salary range']/following::span[1]"
        ).text
except:
salary=""

print("Catchphrase:",catchphrase)
print("Title:",title)
print("Salary:",salary)
print("-----------------------")

driver.back()

time.sleep(3)

driver.quit()
```

---

# 3️⃣ Code flow (simple explanation)

এই script basically:

```
login
   ↓
collect 10 job cards
   ↓
open job
   ↓
click apply
   ↓
scrape info
   ↓
go back
   ↓
next job
```

---

# 4️⃣ Important thing

তোমার দেওয়া selector এর মধ্যে এইটা escape করা হয়েছে:

```
gap-0\.5
```

কারণ **`.` CSS selector এ special character**।

---

# 5️⃣ Next improvement (recommended)

তুমি next step এ add করতে পারো:

✔ pagination (Next button click)

✔ description scraping

✔ CSV save

✔ error handling

✔ WebDriverWait (time.sleep বাদ)

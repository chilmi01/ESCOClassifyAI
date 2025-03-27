from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import re
import time
import json
import nltk
from nltk.tokenize import sent_tokenize

# Constants
LOGIN_URL = "https://login.auth.gr/module.php/core/loginuserpass.php?AuthState=_0f338ce6445552e2f099ae21add67c104adcc2a1b0%3Ahttps%3A%2F%2Flogin.auth.gr%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dhttps%253A%252F%252Fikee.lib.auth.gr%252Fshibboleth%26RelayState%3Dss%253Amem%253Af0fea3aace8f3788755da684a8c986b26c2bc6c98b8cb8227d0e6edeb70b4c71%26cookieTime%3D1733770891"
LIST_PAGE_URL = "https://ikee.lib.auth.gr/search?p=%CE%A4%CE%BC%CE%AE%CE%BC%CE%B1+%CE%9C%CE%B1%CE%B8%CE%B7%CE%BC%CE%B1%CF%84%CE%B9%CE%BA%CF%8E%CE%BD&cc=Postgraduate+Theses&f=&sf=&so=d&of=hb&rg=10&as=0&ln=el&p1=&p2=&p3=&f1=&f2=&f3=&m1=&m2=&m3=&op1=&op2=&sc=0&d1y=0&d1m=0&d1d=0&d2y=0&d2m=0&d2d=0&dt=&jrec=300"
OUTPUT_FILE = "thesis_data_msc_mathsonly.json"
MAX_URLS = 450

USERNAME = ""  # Replace with username
PASSWORD = ""  # Replace with password

# Configure WebDriver
driver = webdriver.Chrome()

def extract_title(text):
    lines = text.splitlines()
    for line in lines:
        words = line.split()[:2]
        if all(re.match(r'[a-zA-Z0-9\s.,?!:;()-]+$', word) for word in words):
            return line.strip()  
    return "No matching line found"

def extract_abstract(text):
    # Remove Greek words
    text_without_greek = re.sub(r'\b[α-ωΑ-Ω]+\b', '', text)

    # Extract meaningful sentences (English words, numbers, and punctuation)
    cleaned_text = ' '.join(re.findall(r'[A-Za-z0-9,.;:\'\"()\[\]!? ]+', text_without_greek)).strip()

    # Tokenize text into sentences
    sentence_list = sent_tokenize(cleaned_text)

    # Remove very short or incomplete sentences (heuristic: keep sentences with at least 5 words)
    meaningful_sentences = [s for s in sentence_list if len(s.split()) > 5]

    # Remove initial "junk" sentences that do not contain a verb (likely meaningless)
    filtered_sentences = []
    for sentence in meaningful_sentences:
        # Check if the sentence contains at least one verb (to ensure it's meaningful)
        if re.search(r'\b(is|was|are|were|be|has|have|had|the|does|do|did|will|shall|can|could|would|should|may|might|must|determine|propose|analyze|evaluate|develop|implement|study|examine|discuss|present|describe|demonstrate)\b', sentence, re.IGNORECASE):
            filtered_sentences.append(sentence)

    # Join back into a paragraph
    final_text = ' '.join(filtered_sentences)

    return final_text


def extract_department(text):
    text_after_uni = text.split('Αριστοτέλειο Πανεπιστήμιο Θεσσαλονίκης, ')[1]
    department_text = re.findall(r'[α-ωΑ-ΩΆ-Ώά-ώ.,]+', text_after_uni)
    return ' '.join(department_text)

# Function to log in
def login(driver, login_url, username, password):
    driver.get(login_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    # Enter credentials
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    # Wait for successful login
    WebDriverWait(driver, 10).until(EC.url_changes(login_url))
    print("Login successful.")

# Function to collect thesis URLs from the list page
def collect_thesis_urls(driver, list_page_url, max_urls):
    driver.get(list_page_url)
    thesis_urls = set()
    current_page = 3

    while len(thesis_urls) < max_urls:
        links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="ikee.lib.auth.gr/record/"][href$="/?ln=el"]')
        for link in links:
            thesis_urls.add(link.get_attribute("href"))

        # Check for "Next" button and navigate
        try:
            if current_page == 2:
                next_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/form[2]/table/tbody/tr/td[2]/a[1]')
            elif current_page >= 3:
                next_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/form[2]/table/tbody/tr/td[2]/a[3]')

            # Click the appropriate "Next" button
            if next_button:
                next_button.click()
                current_page += 1
                time.sleep(1) 
            else:
                print("No more pages.")
                break
        except Exception as e:
            print("No more pages or error occurred:", e)
            break

    print(f"Collected {len(thesis_urls)} thesis URLs.")
    return thesis_urls

# Function to extract thesis details
def extract_thesis_details(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td[align="left"]')))
    time.sleep(1) 
    # Extract details
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, 'td[align="left"]')
        title = elements[0].text if len(elements) > 0 else "Title not found"
        author = elements[1].text if len(elements) > 1 else "Author not found"
        department = elements[3]. text if len(elements) > 2 else "Department not found"
        keywords = elements[6].text if len(elements) > 5 and ',' in elements[5].text and len(elements[5].text) < 100 else "Keywords not found"
        
        abstract_element = driver.find_element(By.CSS_SELECTOR, 'td[align="left"] small')
        abstract = abstract_element.text if abstract_element else "Abstract not found"

        date_element = driver.find_element(By.CSS_SELECTOR, 'td[width="90"] + td')
        date = date_element.text if date_element else "Date not found"
    
        cleaned_abstract = extract_abstract(abstract)
        english_characters = sum(1 for char in cleaned_abstract if char.isalpha() and char.isascii())

        # Skip theses with fewer than 10 English characters
        if english_characters < 200:
            print(f"Skipping thesis at {url} due to insufficient English content in the abstract ({english_characters} characters).")
            return None

        # Clean data
        return {
            "Title": extract_title(title),
            "Author": author,
            "Department": extract_department(department),
            "Degree": "Msc",
            "Abstract": cleaned_abstract,
            "Keywords": keywords,
            "Date": date,
        }
    except Exception as e:
        print(f"Error extracting details for {url}: {e}")
        return None

try:
    login(driver, LOGIN_URL, USERNAME, PASSWORD)
    thesis_urls = collect_thesis_urls(driver, LIST_PAGE_URL, MAX_URLS)
    all_thesis_details = []

    # Extract details for each thesis
    for thesis_url in thesis_urls:
        details = extract_thesis_details(driver, thesis_url)
        if details:
            all_thesis_details.append(details)

    # Save the collected data to a JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(all_thesis_details, json_file, ensure_ascii=False, indent=4)

    print(f"Data saved to {OUTPUT_FILE}")

finally:
    driver.quit()

import time
import random
import logging
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sentence_transformers import SentenceTransformer
from fuzzywuzzy import fuzz

start_time = time.time()


# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load AI model for text similarity
logger.info("Loading AI model for text processing...")
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup Selenium WebDriver
def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# Optimize search queries
def generate_query(person):
    first_name = person["First Name"]
    last_name = person["Last Name"]
    university = person["University"]

    return f'"{first_name} {last_name}" "{university}" site:linkedin.com/in'

# AI-based LinkedIn Title Extraction
def extract_best_title(text):
    if not text:
        return "Not Found"
    
    # Remove unnecessary details
    bad_phrases = ["United States", "Professional Profile", "Connections", "LinkedIn"]
    for phrase in bad_phrases:
        text = text.replace(phrase, "").strip()
    
    # Use Fuzzy Matching to get the best title
    possible_titles = text.split("|")
    best_title = max(possible_titles, key=lambda t: fuzz.token_set_ratio(t, text), default="Not Found").strip()

    return best_title

# Perform search and extract LinkedIn Title
def search_person(person):
    first_name = person["First Name"]
    last_name = person["Last Name"]
    university = person["University"]
    
    if not first_name or not last_name or not university:
        logger.warning("Skipping entry - missing data.")
        return None
    
    query = generate_query(person)
    driver = create_driver()

    try:
        driver.get(f"https://www.bing.com/search?q={query}")
        time.sleep(random.uniform(2, 5))
        elements = driver.find_elements(By.CSS_SELECTOR, "li.b_algo")[:5]

        if not elements:
            logger.warning(f"No results found for {first_name} {last_name}.")
            return None

        for elem in elements:
            try:
                title = elem.find_element(By.TAG_NAME, "h2").text.strip()
                url = elem.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                continue

            if "linkedin.com/in/" in url:
                # Apply AI-based title extraction
                clean_title = extract_best_title(title)
                return {
                    "First Name": first_name,
                    "Last Name": last_name,
                    "University": university,
                    "LinkedIn Title": clean_title,
                    "LinkedIn URL": url
                }
    except Exception as e:
        logger.error(f"Error searching for {first_name} {last_name}: {str(e)}")
        return None
    finally:
        driver.quit()

# Load CSV
input_file = r"names_with_university.csv"
df = pd.read_csv(input_file)
df.fillna("", inplace=True)

# Ensure required columns exist
required_columns = ["First Name", "Last Name", "University"]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

people_list = df.to_dict(orient="records")
results = []

# Run multi-threaded search
logger.info("Starting multi-threaded search...")
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(search_person, person) for person in people_list]
    for future in futures:
        result = future.result()
        if result:
            results.append(result)

# Save results

end_time = time.time()
execution_time = end_time - start_time
print(f"🚀 Total execution time: {execution_time:.2f} seconds")

output_file = r"linkedin_titles.csv"
pd.DataFrame(results).to_csv(output_file, index=False)
logger.info(f"✅ Data saved to {output_file}")

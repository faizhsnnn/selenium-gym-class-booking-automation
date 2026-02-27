from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# ---------------- CONFIG ----------------
ACCOUNT_EMAIL = "student@test.com"
ACCOUNT_PASSWORD = "password123"
GYM_URL = "https://appbrewery.github.io/gym/"

# ---------------- BROWSER SETUP ----------------
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)

wait = WebDriverWait(driver, 5)

# ---------------- RETRY WRAPPER ----------------
def retry(func, retries=5, description="Action"):
    for attempt in range(retries):
        try:
            print(f"Trying {description} (Attempt {attempt + 1})")
            return func()
        except TimeoutException:
            if attempt == retries - 1:
                raise
            time.sleep(1)

# ---------------- LOGIN FUNCTION ----------------
def login():
    login_btn = wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()

    email_input = wait.until(ec.presence_of_element_located((By.ID, "email-input")))
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = wait.until(ec.presence_of_element_located((By.ID, "password-input")))
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)

    submit_btn = driver.find_element(By.ID, "submit-button")
    submit_btn.click()

    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

# ---------------- BOOK FUNCTION ----------------
def book_class(button):
    button.click()
    wait.until(lambda d: button.text in ["Booked", "Waitlisted"])

# ---------------- RUN LOGIN WITH RETRY ----------------
retry(login, description="Login")

# ---------------- BOOK CLASSES ----------------
wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div[id^='class-card-']")))
class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

booked_count = 0
waitlist_count = 0
already_count = 0

for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    if "Tue" in day_title or "Thu" in day_title:
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text

        if "6:00 PM" in time_text:
            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")
            class_info = f"{class_name} on {day_title}"

            if button.text == "Booked":
                print(f"✓ Already booked: {class_info}")
                already_count += 1

            elif button.text == "Waitlisted":
                print(f"✓ Already waitlisted: {class_info}")
                already_count += 1

            elif button.text == "Book Class":
                retry(lambda: book_class(button), description="Booking")
                print(f"✓ Newly booked: {class_info}")
                booked_count += 1
                time.sleep(0.5)

            elif button.text == "Join Waitlist":
                retry(lambda: book_class(button), description="Waitlisting")
                print(f"✓ Joined waitlist: {class_info}")
                waitlist_count += 1
                time.sleep(0.5)

# ---------------- VERIFY BOOKINGS ----------------
total_expected = booked_count + waitlist_count + already_count
print(f"\nExpected bookings: {total_expected}")
print("\nVerifying on My Bookings page...")

def get_my_bookings():
    my_bookings_link = wait.until(ec.element_to_be_clickable((By.ID, "my-bookings-link")))
    my_bookings_link.click()

    wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))

    cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
    if not cards:
        raise TimeoutException("Booking page did not load properly.")
    return cards

all_cards = retry(get_my_bookings, description="Open My Bookings")

verified_count = 0

for card in all_cards:
    try:
        when_text = card.find_element(By.XPATH, ".//p[strong[text()='When:']]").text

        if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
            class_name = card.find_element(By.TAG_NAME, "h3").text
            print(f"✓ Verified: {class_name}")
            verified_count += 1

    except NoSuchElementException:
        pass

print("\n--- FINAL RESULT ---")
print(f"Expected: {total_expected}")
print(f"Verified: {verified_count}")

if total_expected == verified_count:
    print("✅ SUCCESS: All bookings verified!")
else:
    print("❌ Mismatch detected.")

# ---------------- CLEAN EXIT ----------------
driver.quit()
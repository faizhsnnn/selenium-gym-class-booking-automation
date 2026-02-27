# Selenium Gym Class Booking Automation

## Overview

This project automates the login, class selection, booking, and verification process for a gym scheduling platform using Selenium WebDriver.

The automation is designed with stability and reliability in mind, incorporating retry logic, explicit waits, DOM traversal, and booking verification.

Built as part of #90DaysOfCode to demonstrate structured browser automation engineering.

---

## Key Features

- Secure login automation
- Explicit wait-based synchronization
- Retry wrapper for resilience
- Conditional class filtering by day and time
- Smart booking and waitlisting logic
- Post-action verification layer
- Controlled execution and teardown

---

## Technologies Used

- Python
- Selenium WebDriver
- WebDriverWait
- Expected Conditions
- Exception handling strategies

---

## Automation Workflow

1. Launch browser and navigate to gym portal.
2. Login with provided credentials.
3. Identify all class cards.
4. Filter for:
   - Tuesday or Thursday
   - 6:00 PM classes
5. Book or waitlist eligible classes.
6. Track expected booking count.
7. Navigate to "My Bookings".
8. Verify successful reservations.
9. Print summary result.
10. Cleanly terminate browser session.

---

## Stability Enhancements

This automation includes:

- Explicit waits instead of static delays
- Retry wrapper for timeout recovery
- Exception handling for dynamic DOM states
- Verification stage to confirm success
- Controlled browser shutdown

---

## Installation

```bash
pip install selenium
```
Ensure ChromeDriver is compatible with your installed Chrome browser.

Run
```
python main.py
```

---
# Why This Project Matters

This project demonstrates:

Structured automation design

Reliable synchronization strategies

Real-world booking workflow automation

Defensive programming in UI automation

Validation-first automation architecture

It reflects production-style Selenium usage rather than basic scripted interaction.

---
# Author

Faiz Hasan

Python Automation & Backend Developer

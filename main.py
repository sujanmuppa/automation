import os
from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_problem_of_the_day_url():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto('https://www.geeksforgeeks.org/problem-of-the-day')
            page.wait_for_selector('#potd_solve_prob')
            link = page.get_attribute('#potd_solve_prob', 'href')
            browser.close()
            return link if link else "Problem link not found."
    except Exception as e:
        return f"Error fetching problem URL: {e}"

def send_email(problem_url):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')

    subject = "GeeksforGeeks Problem of the Day"
    body = f"Here is the GeeksforGeeks Problem of the Day:\n\n{problem_url}"

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    problem_url = get_problem_of_the_day_url()
    send_email(problem_url)

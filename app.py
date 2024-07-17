from flask import Flask, render_template, request, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyperclip
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_instagram():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to the specific profile
        driver.get('https://www.instagram.com/0.to.life/reels')

        # Wait for the profile page to load
        time.sleep(5)

        # Click on the first video to open it
        first_video_xpath = '(//div[contains(@class, "x1qjc9v5")]//a)[1]'
        first_video_element = driver.find_element(By.XPATH, first_video_xpath)
        first_video_element.click()

        # Wait for the video to load (adjust the sleep time as necessary)
        time.sleep(5)

        # Get the URL of the opened video
        current_url = driver.current_url

        # Locate the description element for the current video
        description_xpath = '//div[@class="_a9zs"]/h1[@class="_ap3a _aaco _aacu _aacx _aad7 _aade"]'
        description_element = driver.find_element(By.XPATH, description_xpath)

        # Extract the description text
        description_text = description_element.text.strip()

        # Copy description to clipboard
        pyperclip.copy(description_text)

        # Download the video using yt-dlp
        ydl_opts = {
            'outtmpl': 'downloaded_video.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([current_url])

        return render_template('result.html', video_url=current_url, description_text=description_text)

    finally:
        driver.quit()

@app.route('/download/<filename>')
def download_video(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

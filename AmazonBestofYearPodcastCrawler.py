# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#from urllib.request import urlopen
import requests
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import random
import os
import pandas as pd
service=Service("D:/Software/chromedriver-win64/chromedriver.exe")
service.start()
driver=webdriver.Remote(service.service_url)
head = "https://music.amazon.com/podcasts/pages/best-of-the-year"
def get_soup(url):
    # Load the webpage
    driver.get(url)
    time.sleep(5)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    driver
    # Get the page source and parse it with BeautifulSoup
    return soup
def get_best_podcasts(url):
# Locate the podcast data section
    soup=get_soup(url)
    podcasts_section = soup.find_all('music-vertical-item')  # Replace with the actual class after inspecting
    podcast_data = []
    for item in podcasts_section:
        try:
            name = item.get("primary-text", "N/A")
            artist = item.get("secondary-text", "N/A")
            url = item.get("primary-href", "N/A")
            image = item.get("image-src", "N/A")
            category = item.find_parent("music-shoveler").get("primary-text", "N/A")

            podcast_data.append({
                "Podcast Name": name,
                "Artist": artist,
                "Category": category,
                "URL": f"https://music.amazon.com{url}" if url.startswith("/") else url,
                "Image": image,
            })
        except Exception as e:
            print(f"Error extracting data for an item: {e}")

    # Create a DataFrame
    df = pd.DataFrame(podcast_data)

    # Save to a CSV file
    df.to_csv("best_of_year_podcasts.csv", index=False)
    return df
if __name__ == "__main__":
    get_best_podcasts(head)

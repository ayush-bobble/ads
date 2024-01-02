import requests
import pandas as pd
from selenium import webdriver

# Function to open URLs in a web browser and capture titles and response codes
def get_title_and_response(click_urls):
    # Create Chrome browser with options
    options = webdriver.ChromeOptions()
    options.headless = True  # Set to True if you want to run in headless mode
    chrome_driver_path = "/usr/lib/chromium-browser/"

    # Start Chrome browser
    browser = webdriver.Chrome(executable_path=chrome_driver_path ,options=options)

    # Initialize lists to store results
    page_titles = []
    response_codes = []

    try:
        for url in click_urls:
            response = requests.get(url)
            response_code = response.status_code

            # Open URL in the browser and get page title
            browser.get(url)
            page_title = browser.title

            # Store results
            page_titles.append(page_title)
            response_codes.append(response_code)

            # You can add additional logic here if needed

        # Close the browser when done with all URLs
        # browser.quit()

    except Exception as e:
        # Handle any exceptions
        print(f"Error: {str(e)}")

    finally:
        # Ensure the browser is closed even if an exception occurs
        browser.quit()

    return page_titles, response_codes

# Function to fetch clickURLs and titles from the API
def fetch_ads_data(api_url):
    response = requests.get(api_url)
    data = response.json()
    ads = data.get("ads", [])
 
    click_urls = [ad.get("clickURL") for ad in ads]
    ad_titles = [ad.get("title") for ad in ads]

    return click_urls, ad_titles

# Main function
def main():
    api_url = "https://api.bobble.ai/v4/ads?limitAdTracking=0&deviceUserAgent=Mozilla%2F5.0%20(Linux%3B%20Android%2012%3B%20SM-A217F%20Build%2FSP1A.210812.016%3B%20wv)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Version%2F4.0%20Chrome%2F111.0.5563.116%20Mobile%20Safari%2F537.36&deviceType=android&appVersion=6440002&clientId=7wZFJWA5chjgat68y826IAIKQ6s197RM&advertisingId=4952ec48-c61f-41be-b55b-346cbf3bbcf5&deviceLanguage=en&sdkVersion=12&deviceModel=SM-A217F&locale=en_IN&deviceManufacturer=samsung&deviceId=57bb2fc3337a63e2&packageName=com.google.android.googlequicksearchbox&placementId=40f16b38-e73f-4d4c-8f49-046f8d6b0c4b&adServerVersion=2"

    click_urls, ad_titles = fetch_ads_data(api_url)
    page_titles, response_codes = get_title_and_response(click_urls)

    # Create a DataFrame and save to Excel
    df = pd.DataFrame({
        'Title of the Ad': ad_titles,
        'ClickURL': click_urls,
        'API Response Code': response_codes,
        'Title of the Page': page_titles
    })
    df.to_excel("ads_data.xlsx", index=False)

if __name__ == "__main__":
    main()

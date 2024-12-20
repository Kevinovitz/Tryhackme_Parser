#########################################################################################
#                                                                                       #
#   Author: Kevinovitz                                                                  #
#   Version: 2.0                                                                        #
#                                                                                       #
#   Description: This script is used to scrape the questions and other information      #
#   from a tryhackme room. It will then add it to a structure and save to a file.       #
#   This file can then be used in for example, Github as a writeup template.            #
#   I did this by hand first, but this should save some time.                           #
#                                                                                       #
#   You need to change the following things:                                            #
#                                                                                       #
#   Default login page                                                                  #
#   Your email adress                                                                   #
#   Your account password                                                               #
#   The default room to scrape from                                                     #
#   Layout of the text                                                                  #
#   The body text with the correct Github link etc.                                     #
#                                                                                       #
#   Changelog:                                                                          #
#   2.1 - Much more reliable search method has been implemented to find all task        #
#         elements without relying on the everchanging "class" property.                #
#         Applies to "task_parent_element" and "task_titles".                           #
#       - Changed the login field names since a new design was made.                    #
#   2.0.1 - The correct selectors have been added again...                              #
#   2.0 - The correct selectors have been added again...                                #
#       - Added some more context to some of the error messages.                        #
#       - Added functionality to remove trailing pieces of text from the questions.     #
#         This text is located in the submit/hint buttons on the page.                  #
#       - Added a progress bar to the console output for fun.                           #
#       - Updated to work with the Advent of Cyber 2024.                                #
#   1.9 - Changed the method of downloading the banner image to use request instead of  #
#         urllib due to some coding warnings by semgrep.                                #
#         Also fixed an issue where the incorrect banner/cover image path was used      #
#         when saving to a local folder instead of a Github repo.                       #
#   1.8 - Found a different method of locating the correct elements which should be     #
#         more robust and not change anymore.                                           #
#   1.7 - Fixed an error where the file wouldn't get written to a file if the file      #
#         didn't already exist.                                                         #
#       - Changed the selectors again...                                                #
#   1.6 - The correct selectors have been added again...                                #
#       - Added functionality to check all relevant elements before parsing the webpage #
#         This ensure no error is given on runtime due to missing elements or wrong     #
#         selectors.                                                                    #
#       - Added functionality to prompt before overwriting a file. This prevents a      #
#         file on github to be altered.                                                 #
#   1.5 - Due to the new site layout, the element selectors changed. Apparently, they   # 
#         they have since changed again. I am not sure if this happens everytime or     #
#         only after a set time.                                                        #
#       - The correct selectors have been added.                                        #
#       - Time to wait before closing selenium instance has been increased to prevent   #
#         an incomplete page from being parsed.                                         #
#       - Added functionality of downloading the banner image when necessary instead    #
#         of only changing the url to a file path.                                      #
#   1.4 - Created variable to link to a github repo instead of hardcoding mine.         #
#   1.3 - Tryhackme changed their website to a new layout, this broke the script.       #
#         Several div/span/img elements where changed in the code to correctly reflect  #
#         the new element on the page.                                                  #
#         Lines: 257, 270, 314, 346, 348                                                #
#                                                                                       #
#########################################################################################

import re
import time
import requests
import os
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

# CHANGE THESE VALUES TO YOUR NEEDS
default_login = 'https://tryhackme.com/login'
email = 'EMAIL_HERE'             # REMOVE THIS WHEN SHARING!!!!
password = 'PASSWORD_HERE'       # REMOVE THIS WHEN SHARING!!!!
default_room = 'https://tryhackme.com/room/encryptioncrypto101'
github_path = ''                 # Add path to you github writeup repo (C:path\\to\\file). Leave blank if you dont want files to be transferred
github_repo = ''                 # Add URL to you github writeup repo (https://github.com/username/repo). Make sure to remove any trailing '/'. Leave blank if you won't upload to github.
write_to_cache = False           # Default is False, when True the resulting parsed webpage will be saved to a temp file.
use_cached = False               # Default is False, when True the cached webpage will be loaded instead of parsing the live website. Usefull for testing purposes.
suffixes = ['SubmitHint','Submit','Complete','Correct AnswerHint','Correct Answer']         # Removes text added to the end of certain questions.

def move_file(destination_path,file_name):
    print('Moving file to new directory.')
    
    # Get the working path and destination folder and add the filename to it
    source_path = os.getcwd()
    file_dest = destination_path + '\\' + file_name
    file_source = source_path + '\\' + file_name

    # Create destination folder if it doesnt already exists
    Path(destination_path).mkdir(exist_ok=True)

    # Copy the file
    shutil.copyfile(file_source,file_dest)

def read_cached_file():

    # Specify the file path
    file_path = 'parsed_page.txt'

    print('Loading cached webpage')    # Progress report

    # Open the file in read mode ('r')
    with open(file_path, 'r', encoding='utf-8') as file:
    # Read the entire contents of the file into a string
        file_contents = file.read()
    
    print('Parsing cached webpage.')    # Progress report

    # Return the parsed data
    soup = BeautifulSoup(file_contents, 'html.parser')
    return soup

def login_with_selenium():
    
    # Load the page, login, and parse the data on the live webpage
    try:
        
        print('Loading Selenium driver.')    # Progress report

        # Create a new instance of the Chrome driver (you can use other browsers too)
        driver = webdriver.Firefox()

        # Open the webpage in the browser
        driver.get(default_login)

        # Wait for it to load
        driver.implicitly_wait(10)

        # Find and fill in the login form fields using the new method
        username_field = driver.find_element(By.NAME, 'usernameOrEmail') # was 'email'
        password_field = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.XPATH, "//*[@type='submit']")  # Replace with the actual name attribute of the submit button

        # Do something with the input fields (e.g., enter values)
        username_field.clear()
        username_field.click()
        username_field.send_keys(email)
        password_field.clear()
        password_field.click()
        # REMOVE PASSWORD WHEN NOT USING FOR A LONGER PERIOD OF TIME OR WHEN SHARING THIS DOCUMENT!!!
        password_field.send_keys(password)
        
        print('Waiting for user to complete captcha challenge.')    # Progress report

        # Add delay so user can complete the Captcha challenge
        # time.sleep(15)

        # Better delay. Check for the Captcha challenge to be completed. Then log in.
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.recaptcha-checkbox-checked")))
        
        # Don't forget to switch back to the main page
        driver._switch_to.default_content()
        
        print('Logging in.')    # Progress report

        # Login
        submit_button.click()

        time.sleep(3)

        #WebDriverWait(driver, 30, 1).until_not(lambda x: x.find_element(By.TYPE, "submit").is_displayed())

        return driver

    except Exception as e:
        print(f"An error occurred: {e}")

def remove_suffix(suffixstring, suffixes):
    for suff in suffixes:
        if suffixstring.endswith(suff):
            return suffixstring.removesuffix(suff)
    return suffixstring

def scrape_webpage_with_selenium(url,driver):

    print('Loading webpage.')    # Progress report

    # Open the webpage in the browser
    driver.get(url)

    # Wait for the page to load (you might need to adjust the time based on your needs)
    driver.implicitly_wait(30)

    # Added another second as it usually exits too fast
    time.sleep(3)

    # Get the HTML content after JavaScript has executed
    page_source = driver.page_source

    # Close the browser
    driver.quit()

    print('Parsing webpage.')    # Progress report

    # Parse the HTML content of the page
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Export the parsed html object to use a cache.
    if write_to_cache:
    
        with open('parsed_page.txt', 'w', encoding='utf-8') as file:
            file.write(str(soup))    

    return soup

# This function doesn't work, but is left in place for reference (to login using cookies instead of manually).
def scrape_authenticated_page(url, cookies):
    # Send an HTTP request to the URL with the provided cookies
    response = requests.get(url, cookies=cookies)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the desired elements using BeautifulSoup methods
        # Replace 'element_selector' with the actual CSS selector of the element you want to scrape
        elements = soup.select('element_selector')

        # Extract and print the text content of each element
        for element in elements:
            print(element.text)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# This function doesn't work, but is left in place for reference (to login using cookies instead of manually).
def get_cookies_with_selenium(login_url, username, password):
    # Create a new instance of the Chrome driver (you can use other browsers too)
    options = Options()
    options.headless = True  # Run the browser in headless mode to hide it from the user
    driver = webdriver.Chrome(options=options)

    # Open the login page in the browser
    driver.get(login_url)

    # Find and fill in the login form fields
    username_field = driver.find_element_by_name('username')  # Replace with the actual name attribute of the username field
    password_field = driver.find_element_by_name('password')  # Replace with the actual name attribute of the password field
    submit_button = driver.find_element_by_name('submit')      # Replace with the actual name attribute of the submit button

    username_field.send_keys(username)
    password_field.send_keys(password)
    submit_button.click()

    # Wait for the login process to complete (you might need to adjust the time based on your needs)
    driver.implicitly_wait(10)

    # Get the cookies after login
    cookies = driver.get_cookies()

    # Close the browser
    driver.quit()

    return cookies

def check_element_presence(page_source):

    error = False

    try:
        page_source.select_one('div.sc-gkKXDf')
    except:
        print('--> The full task element was NOT found on the page! (div.sc-gkKXDf) <--')
        error = True
    
    try:
        page_source.select_one('span.sc-glPjVa')
    except:
        print('--> The task title element was NOT found on the page! (span.sc-glPjVa) <--')
        error = True
    
    try:
        page_source.select_one('div.sc-kCoybQ')
    except:
        print('--> The question task element was NOT found on the page! (div.sc-kCoybQ) <--')
        error = True
    
    try:
        page_source.select_one("meta[property='og:url']")
    except:
        print("--> The url element was NOT found on the page! (meta[property='og:url']) <--")
        error = True
    
    try:
        page_source.find('h1', 'sc-SzDBh')
    except:
        print('--> The room title element was NOT found on the page! (sc-SzDBh)<--')
        error = True
    
    try:
        page_source.select_one("img[alt='Room Banner']")
    except:
        print("--> The room image element was NOT found on the page! (img[alt='Room Banner']) <--")
        error = True
    
    if error:
        print('Some of the elements were not found on the webpage. Exiting..')
        quit()
    else:
        return

def progress(index,len):
    
    progress = '['
    
    for i in range(index + 1):
        progress += 'x'
    
    for i in range(len - index - 1):
        progress += ' '

    progress += ']'
    return progress

if __name__ == "__main__":
    
    # Possible to add custom url
    inputtext = input("Please add the url here. ")

    if not inputtext:
        # Replace 'your_url' with the URL of the webpage you want to scrape
        inputtext = default_room
    
    # Use a cached webpage for faster testing
    if use_cached:

        soup = read_cached_file()

    if not use_cached:
        
        not_logged_in = True
    
        while not_logged_in:

            driver = login_with_selenium()

            # Get the current url
            current_url = driver.current_url

            # Check if log in was successfull
            if current_url == 'https://tryhackme.com/dashboard' or current_url == 'https://tryhackme.com/paths' or current_url == 'https://tryhackme.com/r/dashboard':
                not_logged_in = False
                print("Log in successfull!")

            else:
                print("Something went wrong when trying to login. The current URL doesn't match. Current URL is: " + current_url + " Please try again.")

                # Quit the driver
                driver.quit()
        
        # Set use_cached to true or false. False mean the live webpage will be visited. True means a previously cached version will be used
        soup = scrape_webpage_with_selenium(inputtext,driver)

        check_element_presence(soup)
        
    table_of_contents = ''
    text_questions = '\n'

    # Locate the single parent div with the stable data-* attributes, because the class property constantly changes. This function is commented out below.
    task_parent_element = soup.find('div', {
        'data-sentry-element': 'StyledTaskWrapper',
        'data-sentry-component': 'Tasks',
        'data-sentry-source-file': 'tasks.tsx'
    })

    # Find all child div elements one layer down
    elements = task_parent_element.find_all('div', recursive=False)  # recursive=False ensures only direct children are found

    # Extract the desired elements using BeautifulSoup methods (this should be the entine div of a specific Task n)
    # elements = soup.find_all('div', {'class':'sc-eBAZHg'}) # soup.find_all('div', {'data-sentry-element':'StyledAccordionWrapper'}) # faHdxz                # old site -> elements = soup.select('div.card[id^="task-"]') -> Might change in the future

    # Check if the 'div' element is found before extracting text
    if elements:
        
        print(str(len(elements)) + ' tasks found.') # Output the nr of tasks found on the page.

        for index, element in enumerate(elements):
            
            # print('Processing task ' + str(index) + ' of ' + str(len(elements)) + '.')
            # For each entry check if there is a question which needs an answer. If not, it won't be included in the ToC
            if "Answer format" in str(element):
                #print(element)
                
                progress_bar = progress(index,len(elements)) # create a progress bar for the current elementc

                print(progress_bar + ' Extracting task titles.')    # Progress report
        
                # Find all span elements with data-testid containing 'title-', because the class property constantly changes. This function is commented out below.
                task_titles = element.find_all('span', attrs={'data-testid': re.compile(r'^title-\d+')})

                # Extract the desired elements using BeautifulSoup methods
                # task_titles = element.find_all('span', class_='sc-loOCLO') #  element.find_all('span', {'data-sentry-element':'StyledTaskTitle'}) # gPdIsl, gHZEoh                      # old site -> task_titles = element.select('a.card-link') -> Might change in the future
                
                #print(task_titles)
                # Check if the 'a' element is found before extracting text
                if task_titles:
                    
                    # Extract and print the text content of each task
                    for task_title_element in task_titles:
                        
                        nested_div = task_title_element.find('div')

                        # Extract and print the direct text within the 'a' element after the nested 'div'
                        task_title = ''
                        for content in task_title_element.contents:
                            if content == nested_div:
                                # Stop when reaching the nested 'div'
                                break
                            elif isinstance(content, str):
                                # Collect direct text nodes
                                task_title += content

                        # Check if task_title exists
                        if task_title:

                            #print(f"### {text_content.strip()}\n")

                            # Remove any special characters from the title except for spaces
                            stripped_task_title = re.sub(r"[^ a-zA-Z0-9]+",'',str(task_title.strip()))

                            # Replace all spaces with dashes
                            if ' ' in stripped_task_title:
                                stripped_task_title = str(stripped_task_title.strip()).replace(' ', '-')

                            # Remove all commas
                            if ',' in stripped_task_title:
                                stripped_task_title = str(stripped_task_title.strip()).replace(',', '')

                            text_questions += '### ' + task_title.strip() + '\n\n'
                            table_of_contents += '- [' + str(task_title.strip()) + '](#' + stripped_task_title.lower() + ')\n'

                        else:
                            print("No text directly within the 'a' element.")
                else:
                    print("No Task titles were found.")
                
                questions = element.find_all('div', {'data-sentry-component':'QuestionAndAnswerItem'}) # cyJUJa fKAtdO            # old site -> questions = element.select('div.room-task-question-details') -> Might change in the future
                
                progress_bar = progress(index,len(elements)) # create a progress bar for the current elementc

                print(progress_bar + ' Extracting questions.')    # Progress report

                # Check if the div element is found before extracting text
                if questions:

                    # A question number must preceed the actual question
                    i = 1
                    
                    for question in questions:
                        
                        # Extract text from the div, p, and span elements
                        temp_question = question.get_text(strip=True)#.removesuffix('Submit')                # The new site layout adds 'Submit' to the end of this element.
                        
                        text_question = remove_suffix(temp_question,suffixes)
                        
                        #text_question = temp_question.removesuffix('SubmitHint')                            # The new site layout adds 'SubmitHint' to the end of this element.

                        #print(f"{i}. {div_text}\n\n\n\n   ><details><summary>Click for answer</summary></details>\n")
                        text_questions += str(i) + '. ' + str(text_question) + '\n\n\n\n   ><details><summary>Click for answer</summary></details>\n\n'
                        i = i + 1

                else:
                    print("No questions were extracted, <div> element not found.")
            else:
                progress_bar = progress(index,len(elements)) # create a progress bar for the current elementc
                print(progress_bar + " No answers are required for this task, skipping.")
    else:
        print("No text was extracted, <div> element not found.")

    print('Extracting other information.')    # Progress report

    # Extract other relevant data from the webpage
    url_element = soup.select_one("meta[property='og:url']") # -> Might change in the future
    url = url_element.get('content', '')

    room_code = url.split('/room/',1)[1]
    room_title = soup.find('h1', {'data-sentry-source-file':'room-description.tsx'}).string      # 'sc-iOoWcT jYsxcI'       sc-hBxvHn      # old site -> room_title = soup.find('h1', 'bold-head').string -> Might change in the future

    image_element = soup.select_one("img[alt='Room Banner']")   # old site -> image_element = soup.select_one('img[id=room-image-large]') -> Might change in the future
    image_link = image_element.get('src', '')

    # These lines make up the begin part of the file. From the banner up to the table of contents

    # Check if the image can be directly linked or needs to be downloaded.
    if "tryhackme-images.s3.amazonaws.com" in str(image_link):

        # Create file in current directory if github path is not set
        if github_path:
            # Start of the file with the banner image file
            body_text = '![' + room_title + ' Banner](' + github_repo + '/raw/main/' + room_code + '/' + re.sub(' ','_',room_title) + '_Banner.png)\n\n'
            # Write the the resulting strings to a file
            output_bannername = github_path + '\\' + room_code + '\\' + re.sub(' ','_',room_title) + '_Banner.png'
            # Create destination folder if it doesnt already exists
            Path(github_path + '\\' + room_code).mkdir(exist_ok=True)
        else:
            # Start of the file with the banner image file
            body_text = '![' + room_title + ' Banner](' + re.sub(' ','_',room_title) + '_Banner.png)\n\n'
            # Write the the resulting strings to a file
            output_bannername = re.sub(' ','_',room_title) + '_Banner.png'

        with open(output_bannername, 'wb') as bannerfile:
            for chunk in requests.get(image_link, stream=True).iter_content(chunk_size=128):
                bannerfile.write(chunk)

    else:
        body_text = '![' + room_title + ' Banner](' + image_link + ')\n\n'

    # Use the correct cover image location depending on the save location. Github repo or locally.
    if github_path:
        body_text += '<p align="center">\n   <img src="' + github_repo + '/raw/main/' + room_code + '/' + re.sub(' ','_',room_title) + '_Cover.png" alt="' + room_title + ' Logo">\n</p>\n\n'
    else:
        body_text += '<p align="center">\n   <img src="' + re.sub(' ','_',room_title) + '_Cover.png" alt="' + room_title + ' Logo">\n</p>\n\n'

    body_text += '# ' + room_title + '\n\nThis guide contains the answer and steps necessary to get to them for the [' + room_title + '](' + url + ') room.\n\n'
    body_text += '## Table of contents\n\n'

    print('Writing to file.')    # Progress report

    # Create file in current directory if github path is not set
    if github_path:
        # Write the the resulting strings to a file
        output_filename = github_path + '\\' + room_code + '\\' + room_code + '.md'
        # Create destination folder if it doesnt already exists
        Path(github_path + '\\' + room_code).mkdir(exist_ok=True)
    else:
        # Write the the resulting strings to a file
        output_filename = room_code + '.md'

    if os.path.isfile(output_filename):
        while True:
            try:
                overWrite = input("The file already exists (possibly filled). Would you like to overwrite the file? y = yes, n = no\n")
                if overWrite == "y":
                    with open(output_filename, 'w', encoding='utf-8') as file:
                        file.write(body_text)
                        file.write(table_of_contents)
                        file.write(text_questions)
                    print('Successfully writen to existing file.')   # Progress report
                    break
                if overWrite == "n":
                    print('Skipping saving to file.')   # Progress report
                    break
                else:
                    print('No valid input was given. Please try again.')   # Progress report
            except Exception as e:
                print(f"An error occurred: {e}")
    else:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(body_text)
            file.write(table_of_contents)
            file.write(text_questions)
        print('Successfully writen to file.')   # Progress report

    print('Thank you for using TryhackMe Parser. Come again soon!')   # Progress report

    # # Commands below were used to move the writen file. Now the script writes the files to the right folder in the first place.
    # directory_path = github_path + '\\' + room_code

    # # Move the file to your github repo. This will assume you want the rooms grouped in subfolders.
    # if github_path:
    #     move_file(directory_path,output_filename)


# ====================================================================================================
# The code between here can be used to obtain a cookie for a session and use it to scrape the webpage.
# For now though, this doesn't work and manuall login is implemented.
# Used with scrape_authenticated_page and get_cookies_with_selenium
# ====================================================================================================

# # Replace 'your_login_url', 'your_username', and 'your_password' with the actual values
# login_url = 'your_login_url'
# username = 'your_username'
# password = 'your_password'

# cookies = get_cookies_with_selenium(login_url, username, password)

# # Replace 'your_url' with the URL of the authenticated webpage you want to scrape
# authenticated_url = 'your_url'

# Now you can use the obtained cookies to scrape authenticated pages using requests or selenium
# scrape_authenticated_page('your_authenticated_url', {cookie['name']: cookie['value'] for cookie in cookies})

# ====================================================================================================
# The code between here can be used to obtain a cookie for a session and use it to scrape the webpage.
# For now though, this doesn't work and manuall login is implemented.
# ====================================================================================================
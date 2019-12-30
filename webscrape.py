from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from unidecode import unidecode
import queue, time, json, re
import pandas


def getCard(pointer):
    # find_element_by_xpath returns a selenium object.
    card = {}
    card = dict.fromkeys(keys, None)
    status = browser.find_element_by_xpath("//div[@class='rows text-center']/h1")
    data = browser.find_element_by_xpath("//div[@class='rows text-center']/p")
    data = data.text
    date = data.split('.')[0].split(',')[:2][0][3:]  + data.split('.')[0].split(',')[:2][1]

    # print(status.text)
    #dept = browser.find_element_by_xpath("//*[text()='Department:']")

    card["Case Number"] = code + str(pointer)
    card["Status"] = status.text
    card["Date"] = date

    status_card.append(card)

''' *************************************************START OF THE CODE********************************************************** '''

# Initializing dictionaries and global variables

keys = ["Case Number","Date", "Status"]
code = "YSC"
start = int(input('Starting index -> YSC'))
end = int(input('Ending index -> YSC'))
url = "https://egov.uscis.gov/casestatus"
pointer = start

status_card = []
start = time.time()

# initalizing webdriver
option = webdriver.ChromeOptions()
# option.add_argument("— incognito")
option.add_argument('headless')
option.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')

# Starting the webscraping process
browser = webdriver.Chrome(
    executable_path="./chromedriver", options=option)
print(
    "Crawler has started .... !"
)
# <><><><><><><><><><><><><><Start of the main program loop<><><><><><><><><><><><><><>

while pointer != end:
    browser.get(str(url))
    timeout = 120

    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[@class='mid-logo-visual']")))
        print("I working on it...\n")
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    case_num = browser.find_element_by_css_selector(
    'input[id="receipt_number"]')

    check = browser.find_element_by_css_selector('input[value="CHECK STATUS"]')
    case_num.send_keys(code + str(pointer))
    check.click()

    try:
        WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='logo-sec']")))

        # browser.get_screenshot_as_file('main-page.png')
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
    
    getCard(pointer)
    pointer+=1

'''<><><><><><><><><><>><><><>Dumping the Final Compilation of the code<><><><><><><><>><><><><><><><><><><>'''

with open('data.json', 'w') as outfile:
    json.dump(status_card, outfile, indent=4)

# jsonData = json.loads(status_card)

end = time.time()
exe_time = end - start

print('TOTAL PARSING TIME:', time.strftime("%H:%M:%S", time.gmtime(exe_time)))
print("\n-----OVER-----\n")

browser.quit()
print(json.dumps(status_card, indent=4))
''' *************************************************END OF THE CODE********************************************************** '''

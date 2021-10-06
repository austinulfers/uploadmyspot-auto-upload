from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import logging
import random
import time
import csv
import os

URL = "https://manage.wix.com/dashboard/f332cb86-352a-492f-b04e-c963b4475923/database/data/Upload"

class WixClient:

    def __init__(self, driver: webdriver.chrome.webdriver.WebDriver = None, folder: str = "tmp"):
        """Initializes the client and goes to the upload url.

        Args:
            driver (webdriver.chrome.webdriver.WebDriver, optional): A chrome webdriver. Defaults to None.
            folder (str): folder within cwd to store downloaded files.
        """ 
        self.download_folder = folder
        if driver is None:
            options = webdriver.ChromeOptions()
            prefs = {
                "download.default_directory" : os.path.join(os.getcwd(), folder)
            }
            options.add_experimental_option("prefs", prefs) 
            options.add_argument('log-level=3')
            options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(
                ChromeDriverManager().install(), 
                chrome_options=options
            )
        else:
            self.driver = driver
        self.driver.get(URL)

    def login(self, user: str, pword: str):
        """Logs into the wix login page.

        Args:
            user (str): username
            pword (str): password
        """        
        self.driver.find_element_by_xpath('//*[@id="input_0"]').send_keys(user)
        self.driver.find_element_by_xpath('//*[@id="input_1"]').send_keys(pword)
        self.driver.find_element_by_xpath(
            "/html/body/login-dialog/div/login/div/form/div[3]/div[1]/div[3]/div/button"
        ).click()
        input("Press enter once logged in to continue.")

    def download(self):
        """Downloads the data from content manager as a csv document.
        """        
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(
            '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[1]/div/header/div[2]/div[2]/div[1]/div/button'
            
        ).click()
        self.driver.find_element_by_xpath(
            '/html/body/div[7]/div/div/div/ul/li[2]/span'
        ).click()
        self.driver.find_element_by_xpath(
            '/html/body/div[8]/div/div/div/div/div/div[3]/form/button'
        ).click()

    @staticmethod
    def parse_download(filepath: str = "tmp//Upload.csv", remove: bool = False) -> list:        
        """Parses the download csv from wix and returns the content as a list of
        spots ready for upload.

        Args:
            file (str, optional): downloaded file name. Defaults to 
                "Upload.csv".
            remove (bool, optional): delete the file after parsing. Defaults to 
                False.

        Returns:
            list: list of spots ready for upload
        """
        retry = 5
        while retry > 0:
            if os.path.exists(filepath):
                break
            retry -= 1
            time.sleep(1)
        csvfile = open(filepath, 'r', encoding='utf-8-sig')
        reader = csv.DictReader(csvfile)
        all_spots = []
        for row in reader:
            if row["Completed"] == "":
                spot = {
                    "Agency": row["Agency"],
                    "Client": row["Client"],
                    "First Name": row["First Name"],
                    "Last Name": row["Last Name"],
                    "Destination": row["Destination"],
                    "Additional Recipients": \
                        list(filter(None, [row["Email 1"], row["Email 2"]]))
                }
                for i in range(1, 11):
                    i = str(i)
                    l = row[f"Length {i}"]
                    if i == "1" or l != "":
                        spot.update({
                            "Title": row[f"Title {i}"],
                            "Length": \
                                "" if not l else "0" + l if l[0] == ":" else l,
                            "ISCI": row[f"ID {i}"]
                        })
                        all_spots.append(spot.copy())
        return all_spots, filepath

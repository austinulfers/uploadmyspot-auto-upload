from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
import os

URL = "https://effectv.advertising.comcasttechnologysolutions.com/cad/submit"

class ComcastClient:

    def __init__(self, driver: webdriver.chrome.webdriver.WebDriver = None, folder: str = "tmp"):
        """Initializes the client and goes to the upload url.

        Args:
            driver (webdriver.chrome.webdriver.WebDriver, optional): A chrome webdriver. Defaults to None.
            folder (str): folder within cwd to store downloaded files.
        """ 
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
        """Logs into the Comcast AdDelivery site with passwed credentials.

        Args:
            user (str): username
            pword (str): password
        """        
        self.driver.find_element_by_id("email_login_input").send_keys(user)
        self.driver.find_element_by_id("password_login_input").send_keys(pword)
        self.driver.find_element_by_id("login_login_button").click()

    def clear(self):
        """Clears all text input fields on upload page.
        """        
        self.driver.find_element_by_id(
            "clientName_submit_input"
        ).clear()
        self.driver.find_element_by_id(
            "agencyName_submit_input"
        ).clear()
        self.driver.find_element_by_id(
            "brandName_submit_input"
        ).clear()
        self.driver.find_element_by_id(
            "title_submit_input"
        ).clear()
        self.driver.find_element_by_id(
            "notRequiredIsci_submit_input"
        ).clear()
        self.driver.find_element_by_id(
            "description_submit_input"
        ).clear()
        self.driver.find_element_by_id(
            "additionalRecipients_submit_input"
        ).clear()

    def upload(self, client: str, title: str, duration: str, agency: str = "NA", brand: str = "NA", description: str = "", destination: str = "All Effectv Ops Centers (HD Only)", isci: str = "", recipients: list = [], spot: str = None):
        """Uploads a commercial spot with all the specified information.

        Args:
            client (str): client name
            title (str): title of the spot
            duration (str): duration of the spot in 0:00 format
            agency (str, optional): agent name. Defaults to "NA".
            brand (str, optional): branch name. Defaults to "NA".
            description (str, optional): spot description. Defaults to "".
            destination (str, optional): spot destination. Defaults to "All Effectv Ops Centers (HD Only)".
            isci (str, optional): spot id in isci or ad code. Defaults to "".
            recipients (list, optional): who to notify when spot upload completes. Defaults to [].
            spot (str): filepath to the spot. Defaults to None.
        """
        self.driver.implicitly_wait(5)        
        self.driver.find_element_by_id(
            "clientName_submit_input"
        ).send_keys(client)
        self.driver.find_element_by_id(
            "agencyName_submit_input"
        ).send_keys(agency)
        self.driver.find_element_by_id(
            "brandName_submit_input"
        ).send_keys(brand)
        self.driver.find_element_by_id(
            "title_submit_input"
        ).send_keys(title)
        self.driver.find_element_by_id(
            "notRequiredIsci_submit_input"
        ).send_keys(isci)
        self.driver.find_element_by_id(
            "destination_submit_select"
        ).click()
        self.driver.find_element_by_id(
            "destination_0_submit_option"
        ).click()
        self.driver.find_element_by_id(
            "duration_submit_select"
        ).click()
        if duration == "Other":
            duration_number = "2"
        else:
            duration_number = self._duration_option(duration)
        time.sleep(0.5)
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_id(
            f"duration_{duration_number}_submit_option"
        ).click()
        self.driver.find_element_by_id(
            "description_submit_input"
        ).send_keys(description)
        self.driver.find_element_by_id(
            "additionalRecipients_submit_input"
        ).send_keys(", ".join(recipients))
        if spot is not None:
            self.driver.find_element_by_id(
                "fileInput"
            ).send_keys(spot)

    def _duration_option(self, duration: str) -> str:
        """Returns the duration option from the dropdown menu of the spot upload
            website.

        Args:
            duration (str): duration as exptressed in the mm:ss format.

        Raises:
            Exception: a catch all for any uncaught errors

        Returns:
            str: a number as string representing the option number for the
                duration dropdown.
        """        
        assert ":" in duration, "Duration format error (mm:ss)."
        assert duration.count(":") == 1, "Duration format error (mm:ss)."
        split = duration.split(":")
        seconds = int(split[0]) * 60 + int(split[1])
        assert seconds % 5 == 0, "Duration number error."
        assert seconds > 0, "Duration must be more than 0 seconds."
        assert seconds <= 300, "Duration must be less than 300 seconds."
        if seconds <= 30:
            return str(int(seconds / 5 - 1))
        elif seconds <= 90:
            return str(int(seconds / 15 + 3))
        elif seconds <= 180:
            return str(int(seconds / 30 + 6))
        elif seconds <= 300:
            return str(int(seconds / 30 + 4))
        else:
            raise Exception(
                f"Unkown problem exists with duration number: {duration}"
            )

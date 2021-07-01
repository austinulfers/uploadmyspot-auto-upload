from wix import WixClient
from ad_delivery import ComcastClient
from datetime import datetime
from setup import setup
import configparser
import logging
import os

def main():
    """Executes all main functions.
    """    
    if not os.path.exists(os.path.join("tmp", "Upload.csv")):
        wix = WixClient()
        wix.login(
            config["CREDENTIALS"]["WIX_USERNAME"], 
            config["CREDENTIALS"]["WIX_PASSWORD"]
        )
        wix.download()
    all_spots, filepath = WixClient.parse_download()

    if wix:
        # open new tab so the wix content manager stays open
        wix.driver.execute_script("window.open('');")
        wix.driver.switch_to.window(wix.driver.window_handles[1])
        comcast = ComcastClient(wix.driver)
    else:
        comcast = ComcastClient()
    comcast.login(
        config["CREDENTIALS"]["COMCAST_USERNAME"],
        config["CREDENTIALS"]["COMCAST_PASSWORD"]
    )
    num_spots = len(all_spots)
    for i, spot in enumerate(all_spots):
        comcast.upload(
            client=spot["Client"],
            title=spot["Title"],
            duration=spot["Length"],
            agency=spot["Agency"],
            isci=spot["ISCI"],
            recipients=spot["Additional Recipients"]
        )
        input(f"({i + 1} / {num_spots}) Press any button to continue once the spot has been submitted.")
        comcast.clear()
    input("Application Successfull. Press any button to delete CSV.")
    os.remove(filepath)
    input("CSV Deleted. Press any button to close the application.")
    comcast.driver.close()

if __name__ == "__main__":
    try:
        setup()

        now = datetime.now().strftime("%d-%m-%Y_%H-%M")
        logging.basicConfig(
            filename=f"log/{now}.log", 
            level=logging.DEBUG
        )

        global config
        config = configparser.ConfigParser(interpolation=None)
        config.read('config.ini')   

        main()
    except Exception as e:
        print(e)
        input("Application failed. Read above information to determine root cause.")

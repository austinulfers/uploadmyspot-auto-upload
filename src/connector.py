from wix import WixClient
from ad_delivery import ComcastClient
from datetime import datetime
from setup import setup, check_videos
import configparser
import logging
import os

ATTEMPTS = 100

def main():
    """Executes all main functions.
    """
    for i in range(ATTEMPTS):
        try:
            logging.debug(f"Attempt #{i} for parse_download.")
            all_spots, filepath = WixClient.parse_download()
        except Exception as e:
            logging.error(e)
            input("Press enter to reread the file.")
        else:
            break
    else:
        logging.error("Failed to parse download file in given attempts.")
        raise Exception("Ran out of attempts to parse download file.")

    comcast = ComcastClient()
    comcast.login(
        config["CREDENTIALS"]["COMCAST_USERNAME"],
        config["CREDENTIALS"]["COMCAST_PASSWORD"]
    )
    num_spots = len(all_spots)
    for i, spot in enumerate(all_spots):
        if not spot["Agency"]:
            spot["Agency"] = "NA"
        comcast.upload(
            client=spot["Client"],
            title=spot["Title"],
            duration=spot["Length"],
            agency=spot["Agency"],
            isci=spot["ISCI"],
            recipients=set(spot["Additional Recipients"])
        )
        input(f"({i + 1} / {num_spots}) Press enter to continue once the spot has been submitted.")
        comcast.clear()
    input("Application Successfull. Press enter to delete CSV and end the application.")
    os.remove(filepath)

if __name__ == "__main__":
    try:
        setup()
        for i in range(ATTEMPTS):
            try:
                logging.debug(f"Attempt #{i} for check_videos.")
                check_videos()
            except Exception as e:
                logging.error(e)
                input("Press enter to recheck the videos or continue without them.")
            else:
                break
        else:
            logging.error("Failed to check_videos in given attempts.")
            raise Exception("Ran out of attempts to check_videos.")

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
        logging.error(e)
        print(e)
        input("Application failed. Read above information to determine root cause.")

from wix import WixClient
from ad_delivery import ComcastClient
from datetime import datetime
from setup import setup, check_videos
import configparser
import logging
import os
import traceback
import json
import time

ATTEMPTS = 100

def main():
    """Executes all main functions.
    """
    for i in range(ATTEMPTS):
        try:
            logging.debug(f"Attempt #{i} for parse_download.")
            all_spots, filepath = WixClient.parse_download()
        except Exception:
            trace = traceback.format_exc()
            logging.info(trace)
            print(trace)
            input("Press enter to reread the file.")
        else:
            break
    else:
        logging.info("Failed to parse download file in given attempts.")
        raise Exception("Ran out of attempts to parse download file.")

    comcast = ComcastClient()
    comcast.login(
        config["CREDENTIALS"]["COMCAST_USERNAME"],
        config["CREDENTIALS"]["COMCAST_PASSWORD"]
    )
    time.sleep(float(config["SETUP"]["LOGIN_DELAY"]))
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
            recipients=set(spot["Additional Recipients"]),
            default_recipient=config["UPLOAD"]["DEFAULT_RECIPIENT"]
        )
        input(f"({i + 1} / {num_spots}) Press enter to continue once the spot has been submitted.")
        comcast.clear()
    input("Application Successfull. Press enter to delete CSV and end the application.")
    os.remove(filepath)

if __name__ == "__main__":
    try:
        now = datetime.now().strftime("%d-%m-%Y_%H-%M")
        logging.basicConfig(
            filename=f"log/{now}.log", 
            level=logging.DEBUG
        )

        global config
        config = configparser.ConfigParser(
            interpolation=None, 
            allow_no_value=True
        )
        config.read('config.ini')   

        setup()
        for i in range(ATTEMPTS):
            try:
                logging.debug(f"Attempt #{i} for check_videos.")
                check_videos(
                    allowed_video_formats=json.loads(config["SETUP"]["ALLOWED_VIDEO_FORMATS"]),
                    allowed_video_lengths=json.loads(config["SETUP"]["ALLOWED_VIDEO_LENGTHS"]),
                    frame_tolerance=int(config["SETUP"]["FRAME_TOLERANCE"])
                )
            except Exception as e:
                trace = traceback.format_exc()
                logging.info(trace)
                print(trace)
                input("Press enter to recheck all videos.")
            else:
                break
        else:
            logging.info("Failed to check_videos in given attempts.")
            raise Exception("Ran out of attempts to check_videos.")


        main()
    except Exception as e:
        trace = traceback.format_exc()
        logging.info(trace)
        print(trace)
        input("Application failed. Read above information to determine root cause.")

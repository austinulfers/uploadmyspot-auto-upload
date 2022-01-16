# uploadmyspot-auto-upload

*This automation tool uploads spots to Comcast's AdDelivery portal.*

[![.github/workflows/publish-release.yml](https://github.com/austinulfers/uploadmyspot-auto-upload/actions/workflows/publish-release.yml/badge.svg)](https://github.com/austinulfers/uploadmyspot-auto-upload/actions/workflows/publish-release.yml)
[![wakatime](https://wakatime.com/badge/github/austinulfers/uploadmyspot-auto-upload.svg)](https://wakatime.com/badge/github/austinulfers/uploadmyspot-auto-upload)

## Using the Distributable

To download, visit https://github.com/austinulfers/uploadmyspot-auto-upload/releases and download the latest zip release.

Once your zip file is downloaded, extract all contents into your desired folder. 

1. Here you will see a file called `config.ini.template`. 
2. Within this file, put your login information that will be used for logging into the portals. Feel free to use Notepad or any other text editor to make these changes. 
3. Once you have saved the file with your login information, **remove the `.template` from the filename so that the file name is `config.ini`. This file will be read by the application so it is important that it matches what the application is expecting.
4. The first time you run the executable, it will create a couple of folders (`tmp` and `log`). `tmp` can be used to bypass the initial Wix login if a file called `Upload.csv` is seen within it.
5. Follow the prompts on the command line until the application is completed. Once completed and once the user specifys, the `tmp/Upload.csv` file will be deleted.

All run logs are stored within the `log` folder for use of debugging. 
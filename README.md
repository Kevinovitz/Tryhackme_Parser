# Tryhackme_Parser

## Download

Just download/copy the `tryhackmescraping.py` script and place it anywhere on your system.

## Installation / Preparation

You need some libraries in order for this script to work. Either add them to your python engine or use a venv.

Use requirements.txt. It includes:

- bs4
- requests
- selenium

### Default Installation Instructions

```python
python -m pip install -r requirements.txt
```

### Venv instructions

```python
python -m venv venv

$ pip install -r requirements.txt
```

#### Preparing the script

Now you need to edit the script in order for it to work as you want. Most are placed at the top of the script.

![Thm Parse Script Modify](https://github.com/Kevinovitz/Tryhackme_Parser/raw/main/Images/thm_parser_script_modify.png)

First things to add are your credentials. Use your Tryhackme email and password.

> [!warning]
> **Make sure to remove your credentials if you are not using the script anymore or want to share it with others!**

The Tryhackme login page has been added. Just in case it should ever change. No modification should be necessary for now.

You can change the default room this script will scrape from if you don't supply your own url on script execution. Shouldn't need any change, except if you want to test stuff and don't want to bother with entering a url.

When using Vscode for example, you can add the path to where your synced github files reside. Whenever you run the script, it will automatically save the result to a new folder in your github repo. Just commit and be done with it.

The github repo url is usefull when uploading your files and images to a Github repo. This will add a link to the room cover and banner image.

## Usage

Simply open a terminal or powershell window in the same folder as the script and run it with:

```powershell
python tryhackmescraping.py

or

python .\tryhackmescraping.py
```

When it asks for a room url just can either:

1. Hit enter and let it use its default room (https://tryhackme.com/room/encryptioncrypto101 in this case).
2. Enter a custom url for any tryhackme room like: https://tryhackme.com/room/encryptioncrypto101. Then hit enter.

![Thm Parser Script Start](https://github.com/Kevinovitz/Tryhackme_Parser/raw/main/Images/thm_parser_script_start.png)

The resulting `.md` file can be uploaded to Github. Make sure to check if everything is as it should be. Some textual errors may occur.

![Thm Parser Result](https://github.com/Kevinovitz/Tryhackme_Parser/raw/main/Images/thm_parser_result.png)

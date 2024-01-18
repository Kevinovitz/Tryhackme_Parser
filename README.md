# Tryhackme_Parser

## Download

Just download/copy the `tryhackmescraping.py` script and place it anywhere on your system.

## Installation / Preparation

You need some libraries in order for this script to work. Either add them to your python engine or use a venv.

Use requirements.txt. It includes:

- selenium
- bs4

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

Now you need to edit the script in order for it to work as you want.

First things to add are your credentials

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

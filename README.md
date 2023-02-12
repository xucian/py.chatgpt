<p align="center">
  <img src="img/logo-colorbg.png" />
</p>

# Py ChatGPT
Python app/module mimicking the official ChatGPT app via OpenAI's Completion API.\
Clean and simple, no reverse engineering or hacks in your browser.

Can be ran directly in your console or imported in your python project.

## Requirements
Python 3.10 or up (could work with older versions as well)\
https://www.python.org/downloads

Check that python points to your new installation:\
`which python` (Unix)\
`where python` (Windows CMD)

## Install
1. Open your shell in the current folder

2. Create a virtual environment:\
`python -m venv venv`

3. Activate the venv:\
`. ./venv/Scripts/activate` (Unix)\
`./venv/Scripts/activate.bat` (Windows)

4. Install the requirements:\
`pip install -r requirements.txt`

## Usage
1. Add a `.env` file with `OPENAI_API_KEY="your key"`\
Get yours: https://platform.openai.com/account/api-keys

2. Open your shell in the current folder and run:\
`python chatgpt.py`

## Contribute
This is a work in progress. PRs are welcome! ☕

## Disclaimer
This repo is not associated in any way with OpenAI and it's not an official app.

# ChatGptSlack


## Create a bot for your workspace
Create a bot add to your workspace with the following features:
* Bot
* WebSocket
* app_mentions:read
* chat:write
* reactions:write

Save and secure the bots app token and bot token.

## Configure your python Bot
You'll need to set environment variables for app token and bot token.
`
export SLACK_APP_TOKEN=xapp-1-A04RDPEV5482....
export SLACK_BOT_TOKEN=xoxb-258328483239....
`

## Prepare Selenium target's browser instance

### Windows: start Chrome with remote debugging
Start chrome from your home directory:
`"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=18989 --user-data-dir=c:\users\funky
`
After the browser is loaded, log on to chat gpt and prime the q&a with one question (must not be in the intro page with sample questions)

### Mac: TBD

## Start the bot python script

I am using python 3.11.2

`
pip install -r requirements.txt
python ./chat_gpt_slack.py
`


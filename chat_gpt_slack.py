import os
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


client = WebClient()
api_response = client.api_test()
print(api_response)
opt = Options()
opt.add_experimental_option("debuggerAddress", "127.0.0.1:18989")
selclient = webdriver.Chrome(options=opt)


app_token = os.environ.get("SLACK_APP_TOKEN")
token=os.environ.get("SLACK_BOT_TOKEN")
print("app_token: " + app_token)
print("token: " + token)

# Initialize SocketModeClient with an app-level token + WebClient
client = SocketModeClient(
    # This app-level token will be used only for establishing a connection
    app_token=app_token,  # xapp-A111-222-xyz
    # You will be using this WebClient for performing Web API calls in listeners
    web_client=WebClient(token=token)  # xoxb-111-222-xyz
)

from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        # Add a reaction to the message if it's a new message
        print("payload:" + json.dumps(req.payload, indent = 4))

        if req.payload["event"]["text"].startswith("chatgpt,"):
            client.web_client.reactions_add(
                name="eyes",
                channel=req.payload["event"]["channel"],
                timestamp=req.payload["event"]["ts"],
            )

            input_box = selclient.find_element("xpath", '//textarea[contains(@data-id,"request-:Rdd6:")]')
            #print(input_box)

            input_box.send_keys(req.payload["event"]["text"])

            input_box.send_keys(Keys.RETURN)

            # Wait for answer to finish(no change in answer for 5 sec). look for all <div class="markdown prose ..." ...>
            waits = 0
            chat_gpt_answer = ""
            while waits < 4:
                waits = waits + 1
                time.sleep(1)
                output_box = selclient.find_elements("xpath", '//div[contains(@class,"markdown prose")]')
                tmp_answer = output_box[-1].text
                if chat_gpt_answer != tmp_answer:
                    waits = 0
                    chat_gpt_answer = tmp_answer

            client.web_client.chat_postMessage(channel=req.payload["event"]["channel"], text=chat_gpt_answer)


    if req.type == "interactive" \
        and req.payload.get("type") == "shortcut":
        if req.payload["callback_id"] == "hello-shortcut":
            # Acknowledge the request
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)
            # Open a welcome modal
            client.web_client.views_open(
                trigger_id=req.payload["trigger_id"],
                view={
                    "type": "modal",
                    "callback_id": "hello-modal",
                    "title": {
                        "type": "plain_text",
                        "text": "Greetings!"
                    },
                    "submit": {
                        "type": "plain_text",
                        "text": "Good Bye"
                    },
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "fdsfsdfsdfsdfsdfsdfsdfsd!"
                            }
                        }
                    ]
                }
            )

    if req.type == "interactive" \
        and req.payload.get("type") == "view_submission":
        if req.payload["view"]["callback_id"] == "hello-modal":
            # Acknowledge the request and close the modal
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

# Add a new listener to receive messages from Slack
# You can add more listeners like this
client.socket_mode_request_listeners.append(process)
# Establish a WebSocket connection to the Socket Mode servers
client.connect()
# Just not to stop this process
from threading import Event
Event().wait()

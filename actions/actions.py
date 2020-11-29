# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import requests
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = self.coronaByState(tracker)

        dispatcher.utter_message(text=message)

        return []

    def coronaByState(self, tracker):
        api_address = 'https://api.covid19india.org/data.json'

        response = requests.get(api_address).json()

        entities = tracker.latest_message['entities']
        print("Last message now ", entities)
        state = None
        for e in entities:
            if e['entity'] == "state":
                state = e['value']

        message = "Please enter the correct state name"
        for data in response["statewise"]:
            if data["state"] == state.title():
                message = "Active: " + data["active"] + " Confirmed: " + data["confirmed"] + \
                    " Recovered: " + data["recovered"] + \
                    " On " + data["lastupdatedtime"]

        return message

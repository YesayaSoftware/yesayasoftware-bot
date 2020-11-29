import requests

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionLatestPost(Action):

    def name(self) -> Text:
        return "action_latest_post"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = self.latestPosts(tracker)

        for data in response:
            dispatcher.utter_message(
                text=data["title"],
                image=data["thumbnail_url"]
            )

        return []

    def latestPosts(self, tracker):
        api_address = 'http://yesayasoftware.test/api/posts'

        response = requests.get(api_address).json()

        entities = tracker.latest_message['entities']
        
        category = None

        for e in entities:
            if e['entity'] == "category":
                category = e['value']

        return response

from typing import Any, Dict, Text, List

from rasa_sdk import Tracker
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, SlotSet


# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class MyForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_my_form"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> List[EventType]:
        result = await super().run(dispatcher, tracker, domain)
        slots = tracker.slots

        has_all_slots = (await self.next_requested_slot(dispatcher, tracker, domain)).get("value") is None

        dispatcher.utter_message(text=f'-- Name: {slots.get("name")}')
        dispatcher.utter_message(text=f'-- From: {slots.get("from")}')
        dispatcher.utter_message(text=f'-- Hungry: {slots.get("hungry")}')

        if has_all_slots:
            dispatcher.utter_message(text=f'You\'ve finished the form! Clearing the values...')
            result.append(SlotSet('name', None))
            result.append(SlotSet('from', None))
            result.append(SlotSet('hungry', None))

        return result

    async def extract_hungry(self,
                              dispatcher: CollectingDispatcher,
                              tracker: Tracker,
                              domain: DomainDict,
                              ) -> Dict[Text, Any]:
        next_slot = (await self.next_requested_slot(dispatcher, tracker, domain)).get("value")
        value = None

        # This could be defined in the domain.yml file
        # but is shown here to show Rasa API.
        if next_slot == "hungry":
            intent = tracker.get_intent_of_latest_message()
            if intent == "affirm":
                value = True
            elif intent == "deny":
                value = False

        if value is None:
            value = tracker.slots.get("hungry")

        return {
            "hungry": value
        }

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> List[Text]:
        return [
            "name", "from", "hungry"
        ]

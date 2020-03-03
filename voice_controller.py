import threading
from time import sleep, time
from typing import Callable, Dict, List

from basic_speech_to_text import speech_to_text, is_wake_up_word_said
from plant_intent_recognizer.detect_intent import RasaIntent, Intent

CALLBACK_INTENTS: Dict[Intent, List[Callable[[], None]]] = {}


def register_function_for_intent(intent: Intent):
    """Register a function to be called every time an intent is detected by VoiceController"""
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            response = f(*args, **kwargs)
            return response

        print(f"Registering {f} for intent: {intent.value}")
        functions = CALLBACK_INTENTS.get(intent, [])
        function.append(f)
        CALLBACK_INTENTS[intent] = functions
        return wrapped

    return inner_decorator


def _trigger_function_on_intent(intent: Intent):
    """Trigger all function registered for this intent"""
    if intent not in CALLBACK_INTENTS:
        return
    functions = CALLBACK_INTENTS[intent]
    for f in functions:
        f()


class VoiceController:
    def __init__(self, active_time_delay=10):
        """
        :param active_time_delay time in seconds after the keyword wa said before being not "active"
        """

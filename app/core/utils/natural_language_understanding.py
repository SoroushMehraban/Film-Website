from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from django.conf import settings

authenticator = IAMAuthenticator(settings.IBM_NLU_API_KEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(settings.IBM_NLU_URL)


def is_violent(text, threshold):
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(emotion=EmotionOptions())).get_result()
    anger = response['emotion']['document']['emotion']['anger']
    return anger > threshold

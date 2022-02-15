from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.conf import settings

authenticator = IAMAuthenticator(settings.IBM_S2T_API_KEY)
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)
speech_to_text.set_service_url(settings.IBM_S2T_URL)


def get_text(audio_file, content_type):
    result = speech_to_text.recognize(
        audio=audio_file,
        content_type=content_type,
        model='en-US_BroadbandModel').get_result()
    transcript = result['results'][0]['alternatives'][0]['transcript']
    return transcript

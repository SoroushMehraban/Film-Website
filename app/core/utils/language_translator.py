from django.conf import settings
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(settings.IBM_TRANSLATE_API_KEY)
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

language_translator.set_service_url(settings.IBM_TRANSLATE_URL)


def translate_comment(text, lang):
    translation = language_translator.translate(
        text=text,
        model_id=f'en-{lang}').get_result()
    return translation['translations'][0]['translation']

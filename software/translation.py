from modeltranslation.translator import translator, TranslationOptions
from .models import Software

class SoftwareTranslationOptions(TranslationOptions):
    fields = ('name', 'description')  # fields you want translated

translator.register(Software, SoftwareTranslationOptions)

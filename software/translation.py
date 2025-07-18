# software/translation.py

from modeltranslation.translator import translator, TranslationOptions
from .models import Software, Category # Import BOTH Software AND Category models

# Translation options for the Software model
class SoftwareTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'homepage_description', 'requirements',) # Added other relevant fields from your model for completeness
    # Add other translatable fields from your Software model if you want them translated

translator.register(Software, SoftwareTranslationOptions)

# Translation options for the Category model (THIS IS THE MISSING PART)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',) # Specify that the 'name' field of Category should be translated

translator.register(Category, CategoryTranslationOptions)

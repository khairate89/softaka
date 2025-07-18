# software/middleware.py

from django.utils import translation
import logging

logger = logging.getLogger(__name__) # Initialize a logger for this module

class ForceAdminEnglishMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the incoming request path
        logger.info(f"Middleware: Processing request for path: {request.path}")

        # Store the original language (if set by LocaleMiddleware)
        original_language = getattr(request, 'LANGUAGE_CODE', None)
        if original_language:
            logger.info(f"Middleware: Original language for this request: {original_language}")

        # Check if the path starts with /admin/
        if request.path.startswith('/admin/'):
            logger.info(f"Middleware: Admin path detected! Forcing language to 'en'.")
            translation.activate('en')
            # Also set request.LANGUAGE_CODE for consistency
            request.LANGUAGE_CODE = 'en'
            # Flag that we forced the language
            request._admin_language_forced = True
            logger.info(f"Middleware: Language after force: {translation.get_language()}")
        
        response = self.get_response(request)

        # If language was forced for admin, revert to original language for the response processing
        if getattr(request, '_admin_language_forced', False) and original_language:
            logger.info(f"Middleware: Reverting language from 'en' to '{original_language}' for response.")
            translation.activate(original_language)
            request.LANGUAGE_CODE = original_language

        return response
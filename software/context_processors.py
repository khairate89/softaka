# software/context_processors.py

from .models import Category

def menu_categories(request):
    """
    Context processor to make different sets of categories available in templates.
    """
    # Categories for the left sidebar (already existing)
    sidebar_categories = Category.objects.filter(display_on_menu=True).order_by('name')
    
    # NEW: Categories for the main header navigation
    header_categories = Category.objects.filter(display_on_header=True).order_by('name')

    return {
        'all_categories_data': sidebar_categories, # For the left sidebar
        'header_categories': header_categories,    # NEW: For the header navigation
    }
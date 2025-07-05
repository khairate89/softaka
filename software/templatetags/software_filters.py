from django import template
import re

register = template.Library()

@register.filter
def remove_img_tags(html_string):
    """
    Removes <img> tags and then cleans up any resulting empty paragraphs
    or figure tags from an HTML string.
    """
    # 1. Remove <img> tags (case-insensitive, non-greedy match)
    clean_html = re.sub(r'<img[^>]*?>', '', html_string, flags=re.IGNORECASE)

    # 2. Remove common empty block elements that might have contained images
    #    or were left behind, especially from CKEditor.
    #    This regex targets <p> and <figure> tags that are empty or contain only whitespace.
    clean_html = re.sub(r'(<p>\s*</p>|<p>&nbsp;</p>|<figure[^>]*?>\s*</figure>)', '', clean_html, flags=re.IGNORECASE)

    # Optional: You might also want to remove other specific empty tags like <div> if they're causing issues.
    # For example, to remove empty <div>s:
    # clean_html = re.sub(r'<div>\s*</div>', '', clean_html, flags=re.IGNORECASE)

    return clean_html
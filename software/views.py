# software/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.db import IntegrityError  # <--- MAKE SURE THIS LINE IS PRESENT
from django.contrib import messages # NEW: Import messages framework
# IMPORTANT: All models are imported here, including the new ones
from .models import Software, Category, SoftwareVersion, DownloadLink, SoftwareDownloadPageVersion, DownloadPageSpecificLink, Comment
# NEW: Import CommentForm
from .forms import CommentForm
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # <== You forgot this
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber # <--- ADD THIS IMPORT
from django.core.validators import validate_email      # <--- ADD THIS LINE
from django.core.exceptions import ValidationError  # <--- ADD THIS LINE
from .models import Rating
from decimal import Decimal

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    software_list = Software.objects.filter(category=category).order_by('-created_at')
    
    context = {
        'category': category,
        'software_list': software_list,
        # ... (other context variables)
    }
    return render(request, 'software/category_detail.html', context)
class SearchResultsView(ListView):
    model = Software
    template_name = 'software/search_results.html'
    context_object_name = 'software_list'
    paginate_by = 9

    def get_queryset(self):
        self.query = self.request.GET.get('q', '')  # Save query to self
        if self.query:
            return Software.objects.filter(
                Q(name__icontains=self.query) |
                Q(description__icontains=self.query)
            ).select_related('category').prefetch_related('versions')
        return Software.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query  # Pass query into template
        return context


class SoftwareListView(ListView):
    model = Software
    template_name = 'software/index.html'
    context_object_name = 'software_list'
    paginate_by = 9
    ordering = ['-created_at']

    def get_queryset(self):
        # Prefetch the current version for each software if you need it on the homepage
        return super().get_queryset().select_related('category').prefetch_related(
            'versions'
        )

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


class SoftwareDetailView(DetailView):
    model = Software
    template_name = 'software/software_detail.html'
    context_object_name = 'software'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return get_object_or_404(
            queryset.select_related('category')
                    .prefetch_related(
                        'versions__download_links',
                        'download_page_versions__specific_download_links',
                        'comments' # NEW: Prefetch comments for this software
                    ),
            category__slug=self.kwargs.get('category_slug'),
            slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        software = self.get_object()

        current_version = software.versions.filter(is_current_version=True).first()
        context['current_version'] = current_version

        download_page_version_obj = software.download_page_versions.order_by('-release_date').first()
        context['download_page_version_obj'] = download_page_version_obj

        relevant_products = Software.objects.filter(
            category=software.category
        ).exclude(pk=software.pk).order_by('?')[:5].select_related('category')
        context['relevant_products'] = relevant_products

        # NEW: Add comment form to context for GET requests or invalid POST requests
        context['comment_form'] = CommentForm() 
        
        # NEW: Fetch approved comments for this software
        context['comments'] = Comment.objects.filter(
            software=software,
            approved_comment=True
        ).order_by('-created_at') # Order by newest first

        return context

    def post(self, request, *args, **kwargs):
        # Retrieve the software object first
        self.object = self.get_object() 
        software = self.object # Assign to software for clarity

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # Create comment instance but don't save to DB yet
            comment.software = software # Link comment to the current software
            comment.save() # Save the comment (approved_comment is False by default)
            messages.success(request, 'Thank you for your comment! It will appear after approval by an administrator.') # NEW: Success message
            return redirect(software.get_absolute_url()) # Redirect back to the software detail page
        else:
            messages.error(request, 'Please correct the errors below.') # NEW: Error message for invalid form
            context = self.get_context_data(object=self.object) # Get context with existing data
            context['comment_form'] = form # Pass the form with errors back to the template
            return self.render_to_response(context)


class CategorySoftwareListView(ListView):
    model = Software
    template_name = 'software/category_software_list.html'
    context_object_name = 'software_list'
    paginate_by = 9

    def get_queryset(self):
        return Software.objects.filter(
            category__slug=self.kwargs.get('slug')
        ).select_related('category').prefetch_related('versions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return context


class FileDownloadView(TemplateView):
    template_name = 'software/file_download.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        version_id = self.request.GET.get('id') 
        
        if not version_id:
            raise Http404("Download Page Version ID not provided.")

        try:
            software_download_page_version = get_object_or_404(
                SoftwareDownloadPageVersion.objects.select_related('software')
                                                   .prefetch_related('specific_download_links'),
                pk=version_id
            )
            context['software_download_page_version'] = software_download_page_version
            context['software'] = software_download_page_version.software 
            
        except Http404:
            raise
        except Exception as e:
            print(f"Error in FileDownloadView: {e}") 
            raise Http404("An unexpected error occurred while fetching download details.")

        return context
    import json

from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Software, Rating

@require_POST

def rate_software(request):
    try:
        data = json.loads(request.body)
        software_id = data.get('software_id')
        score = int(data.get('score'))

        software = get_object_or_404(Software, id=software_id)

        Rating.objects.update_or_create(
            software=software,
            user=request.user if request.user.is_authenticated else None,
            defaults={'score': score}
        )

        software.refresh_from_db()

        return JsonResponse({
            'success': True,
            'average_rating': str(round(software.average_rating, 2)),
            'total_ratings': software.total_ratings
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

# You might want a NewsletterSubscriber model later, but for now, this works
# from .models import NewsletterSubscriber # Example: if you had a model to save emails

@require_POST
def subscribe_newsletter(request):
    email = request.POST.get('email')

    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email address cannot be empty.'}, status=400)

    try:
        # Basic email format validation
        validate_email(email)
    except ValidationError:
        return JsonResponse({'status': 'error', 'message': 'Please enter a valid email address.'}, status=400)

    try:
        # Attempt to create the new subscriber
        NewsletterSubscriber.objects.create(email=email)
        print(f"Successfully subscribed: {email}") # For your console log
        return JsonResponse({'Thank you for subscribing to our newsletter!'})
    except IntegrityError:
        # This specific error occurs if the email (which is unique=True) already exists
        print(f"Attempted to subscribe duplicate email: {email}") # For your console log
        return JsonResponse({'status': 'info', 'message': 'This email address is already subscribed.'})
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred during subscription for {email}: {e}") # For your console log
        return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred. Please try again later.'}, status=500)


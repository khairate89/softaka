from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = 'software'
urlpatterns = [
    path('', views.SoftwareListView.as_view(), name='index'),
    path('search/', views.SearchResultsView.as_view(), name='search-results'),
    path('category/<slug:slug>/', views.CategorySoftwareListView.as_view(), name='category-software-list'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # URL pattern for software detail uses category_slug and software slug
    path('<slug:category_slug>/<slug:slug>/', views.SoftwareDetailView.as_view(), name='software-detail'),
    path('file-download/', views.FileDownloadView.as_view(), name='file-download'),
    path('rate-software/', views.rate_software, name='rate_software'),
    path('', TemplateView.as_view(template_name='software/index.html'), name='home'),
    path('dmca/', TemplateView.as_view(template_name='software/dmca.html'), name='dmca'),
    path('disclaimer/', TemplateView.as_view(template_name='software/disclaimer.html'), name='disclaimer'),
    path('privacy-policy/', TemplateView.as_view(template_name='software/privacy_policy.html'), name='privacy_policy'),
    path('terms-conditions/', TemplateView.as_view(template_name='software/terms_conditions.html'), name='terms_conditions'),
    path('sitemap-page/', TemplateView.as_view(template_name='software/sitemap_page.html'), name='sitemap_page'),
    path('contact-us/', TemplateView.as_view(template_name='software/contact_us.html'), name='contact_us'),
    path('about-us/', TemplateView.as_view(template_name='software/about_us.html'), name='about_us'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

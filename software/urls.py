# software/urls.py

from django.urls import path
from . import views

app_name = 'software'

urlpatterns = [
    path('', views.SoftwareListView.as_view(), name='index'),
    path('search/', views.SearchResultsView.as_view(), name='search-results'),
    path('category/<slug:slug>/', views.CategorySoftwareListView.as_view(), name='category-software-list'),
    path('<slug:category_slug>/<slug:slug>/', views.SoftwareDetailView.as_view(), name='software-detail'),
    
    # CHANGE THIS LINE: Remove the <slug:slug>/ from the path
    path('file-download/', views.FileDownloadView.as_view(), name='file-download'), # Now just 'file-download/'
    path('rate-software/', views.rate_software, name='rate_software'),

]


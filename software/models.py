# software/models.py

from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal


# Import ImageSpecField and processors for image resizing
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Import for Rating model and validators
from django.conf import settings # Needed for AUTH_USER_MODEL
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Font Awesome icon class (e.g., 'fas fa-desktop')")
    display_on_menu = models.BooleanField(default=True, help_text="Check to display this category in the **left sidebar menu**.")
    display_on_header = models.BooleanField(default=False, help_text="Check to display this category in the **main header navigation**.")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('software:category-software-list', kwargs={'slug': self.slug})


class Software(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='software_items')
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    license_type = models.CharField(max_length=100, blank=True, null=True)
    file_size = models.CharField(max_length=50, blank=True, null=True)
    website_link = models.URLField(max_length=500, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    homepage_description = models.TextField(blank=True, null=True, help_text="A short description for the homepage.")
    requirements = RichTextUploadingField(blank=True, null=True, help_text="System requirements for the software.")
    image = models.ImageField(upload_to='software_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Fields for ratings summary
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_ratings = models.IntegerField(default=0)

    # Imagekit for thumbnail
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(100, 100)],
                                     format='PNG',
                                     options={'quality': 90})

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Software"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('software:software-detail', kwargs={'category_slug': self.category.slug, 'slug': self.slug})

    # Method to update average rating and total ratings
    def update_ratings_summary(self):
        ratings = self.ratings.all()
        self.total_ratings = ratings.count()
        if self.total_ratings > 0:
            # Use Decimal for calculation to maintain precision
            total_score = sum(r.score for r in ratings)
            self.average_rating = Decimal(total_score) / Decimal(self.total_ratings)
        else:
            self.average_rating = Decimal('0.00') # Use Decimal for consistency
        self.save(update_fields=['average_rating', 'total_ratings'])


class SoftwareVersion(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50)
    release_date = models.DateField(blank=True, null=True)
    download_link_url = models.URLField(max_length=500, blank=True, null=True, help_text="Direct download URL for this version (optional if using specific links).")
    is_current_version = models.BooleanField(default=False, help_text="Only one version should be marked as current per software.")

    class Meta:
        ordering = ['-release_date', '-version_number']
        unique_together = ('software', 'version_number')

    def __str__(self):
        return f"{self.software.name} - v{self.version_number}"

    def save(self, *args, **kwargs):
        if self.is_current_version:
            # Ensure only one version is current for this software
            SoftwareVersion.objects.filter(software=self.software).exclude(pk=self.pk).update(is_current_version=False)
        super().save(*args, **kwargs)


class DownloadLink(models.Model):
    version = models.ForeignKey(SoftwareVersion, on_delete=models.CASCADE, related_name='download_links')
    name = models.CharField(max_length=200, help_text="e.g., 'Direct Download', 'Mirror 1'")
    url = models.URLField(max_length=500)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        unique_together = ('version', 'name') # Ensures unique link names per version

    def __str__(self):
        return f"{self.name} ({self.version.software.name} v{self.version.version_number})"


class SoftwareDownloadPageVersion(models.Model):
    # Foreign key to Software model. The related_name 'download_page_versions' is used by Software
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='download_page_versions')
    version_number = models.CharField(max_length=50, help_text="Version number associated with this specific download page.")
    display_title = models.CharField(max_length=255, blank=True, help_text="Title for this download page version (e.g., 'v1.0 Installer').")
    release_date = models.DateField(blank=True, null=True)
    notes = RichTextUploadingField(blank=True, null=True, help_text="Specific notes or changes for this download page version.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-release_date', '-version_number']
        unique_together = ('software', 'version_number')
        verbose_name = "Software Download Page Version"
        verbose_name_plural = "Software Download Page Versions"

    def __str__(self):
        return f"{self.software.name} - Download Page for v{self.version_number}"


class DownloadPageSpecificLink(models.Model):
    version_for_page = models.ForeignKey(SoftwareDownloadPageVersion, on_delete=models.CASCADE, related_name='specific_download_links')
    name = models.CharField(max_length=200, help_text="Descriptive name for this specific download.")
    url = models.URLField(max_length=500, help_text="The URL for this specific download.")
    file_size = models.CharField(max_length=50, blank=True, null=True, help_text="File size (e.g., '150 MB', '2.3 GB').")
    order = models.PositiveIntegerField(default=0, help_text="Order in which these links are displayed on the download page.")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Download Page Specific Link"
        verbose_name_plural = "Download Page Specific Links"
        unique_together = ('version_for_page', 'name')

    def __str__(self):
        return f"{self.name} for {self.version_for_page.software.name} v{self.version_for_page.version_number}"


# Comment model
class Comment(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, help_text="Name of the commenter.")
    email = models.EmailField(blank=True, null=True, help_text="Email of the commenter (optional).")
    content = models.TextField(help_text="The comment text.")
    created_at = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False, help_text="Only approved comments will be displayed.")

    class Meta:
        ordering = ['created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.name} on {self.software.name}"


# Rating model (Simplified for public ratings without IP tracking)
class Rating(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text="The logged-in user who submitted the rating (optional for anonymous ratings).")
    # ip_address field REMOVED for simplified public ratings
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 (lowest) to 5 (highest) stars."
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Removed unique_together = ('software', 'ip_address')
        # This allows multiple anonymous ratings. If an authenticated user rates,
        # the RateSoftwareView will handle updating their single rating.
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return f"{self.software.name} - {self.score} stars by {self.user.username if self.user else 'Anonymous'}"


# Signals to update Software's aggregate ratings whenever a Rating is saved or deleted
@receiver(post_save, sender=Rating)
def update_software_ratings_on_save(sender, instance, **kwargs):
    # Use transaction.on_commit to ensure it runs after the Rating is fully committed
    # This can prevent issues with partial database state during signal execution
    from django.db import transaction
    transaction.on_commit(lambda: instance.software.update_ratings_summary())

@receiver(post_delete, sender=Rating)
def update_software_ratings_on_delete(sender, instance, **kwargs):
    from django.db import transaction
    transaction.on_commit(lambda: instance.software.update_ratings_summary())
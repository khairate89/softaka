from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal

# Import for Cloudinary
from cloudinary.models import CloudinaryField

# Import for Rating model and validators
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Font Awesome icon class (e.g., 'fas fa-desktop')")
    display_on_menu = models.BooleanField(default=True, help_text="Check to display this category in the **left sidebar menu**.")
    display_on_header = models.BooleanField(default=False, help_text="Check to display this category in the **main header navigation**.")
        # New SEO fields
    meta_title = models.CharField(_("Meta Title"), max_length=255, blank=True, null=True,
        help_text=_("Optional. Title for SEO, defaults to category name."))
    meta_description = models.TextField(_("Meta Description"), blank=True, null=True,
        help_text=_("Optional. Description for SEO."))
      # New multilingual description fields
    description_en = models.TextField(_("Description [en]"), blank=True, null=True)
    description_fr = models.TextField(_("Description [fr]"), blank=True, null=True)
    description_de = models.TextField(_("Description [de]"), blank=True, null=True)
    description_es = models.TextField(_("Description [es]"), blank=True, null=True)
    description_ar = models.TextField(_("Description [ar]"), blank=True, null=True)
    description_ru = models.TextField(_("Description [ru]"), blank=True, null=True)
    description_zh_hans = models.TextField(_("Description [zh-hans]"), blank=True, null=True)
# This is the corrected field
    is_published = models.BooleanField(default=True, help_text=_("Whether this category should be publicly visible."))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("The date and time this category was last updated."))
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
    is_published = models.BooleanField(default=True, help_text=_("Whether this software should be publicly visible."))
    # Cloudinary image field replacing ImageField
    image = CloudinaryField('image', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Fields for ratings summary
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_ratings = models.IntegerField(default=0)

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

    def update_ratings_summary(self):
        ratings = self.ratings.all()
        self.total_ratings = ratings.count()
        if self.total_ratings > 0:
            total_score = sum(r.score for r in ratings)
            self.average_rating = Decimal(total_score) / Decimal(self.total_ratings)
        else:
            self.average_rating = Decimal('0.00')
        self.save(update_fields=['average_rating', 'total_ratings'])

    # Optional: return Cloudinary thumbnail URL (200x200)
    def image_thumbnail_url(self):
        if self.image:
            # Cloudinary supports transformations via URL, e.g. resize to 200x200
            return self.image.build_url(width=200, height=200, crop='fill')
        return None


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
            SoftwareVersion.objects.filter(software=self.software).exclude(pk=self.pk).update(is_current_version=False)
        super().save(*args, **kwargs)


class DownloadLink(models.Model):
    version = models.ForeignKey(SoftwareVersion, on_delete=models.CASCADE, related_name='download_links')
    name = models.CharField(max_length=200, help_text="e.g., 'Direct Download', 'Mirror 1'")
    url = models.URLField(max_length=500)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        unique_together = ('version', 'name')

    def __str__(self):
        return f"{self.name} ({self.version.software.name} v{self.version.version_number})"


class SoftwareDownloadPageVersion(models.Model):
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


class Rating(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text="The logged-in user who submitted the rating (optional for anonymous ratings).")
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 (lowest) to 5 (highest) stars."
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return f"{self.software.name} - {self.score} stars by {self.user.username if self.user else 'Anonymous'}"


@receiver(post_save, sender=Rating)
def update_software_ratings_on_save(sender, instance, **kwargs):
    from django.db import transaction
    transaction.on_commit(lambda: instance.software.update_ratings_summary())


@receiver(post_delete, sender=Rating)
def update_software_ratings_on_delete(sender, instance, **kwargs):
    from django.db import transaction
    from software.models import Software # Import Software model here to avoid circular dependencies
    
    try:
        software = instance.software
        transaction.on_commit(lambda: software.update_ratings_summary())
    except Software.DoesNotExist:
        # The software object was likely deleted in a cascading manner.
        # We can safely ignore this as there's nothing to update.
        pass


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Subscription Date"))

    class Meta:
        verbose_name = _("Newsletter Subscriber")
        verbose_name_plural = _("Newsletter Subscribers")
        ordering = ['-timestamp']

    def __str__(self):
        return self.email

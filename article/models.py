import uuid
from django.db import models
from django.utils import timezone
from tinymce import models as tinymce_models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_modify_time = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Article(BaseModel):
    """
    Model for storing article data
    """
    STATUS_ARTICLE_CHOICES = [
        ("pe", "Pending"),
        ("pu", "Published"),
        ("re", "Rejected"),
    ]

    title = models.CharField(verbose_name=_('Title'),
                             max_length=100,
                             unique=True)
    body = tinymce_models.HTMLField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    image = models.ImageField(upload_to='article_img',
                              null=True, blank=True,
                              default='article_img/default_article.svg')
    status = models.CharField(max_length=2,
                              choices=STATUS_ARTICLE_CHOICES,
                              default='pe')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        db_table_comment = "Article table braviss"
        get_latest_by = 'created_at'

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from core.models import TechStack


class FeaturedProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(featured=True)


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to="project_images/", blank=True, null=True)
    tech_stacks = models.ManyToManyField(
        TechStack,
        related_name="projects",
        blank=True,
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = RichTextField()
    demo_link = models.URLField(blank=True, null=True)
    source_code = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)

    objects = models.Manager()
    featured_projects = FeaturedProjectManager()

    class Meta:
        ordering = ["-id"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name

    @property
    def is_open_source(self):
        return bool(self.source_code)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProjectKeyFeature(models.Model):
    short_description = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project,
        related_name="key_features",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Project Key Feature"
        verbose_name_plural = "Project Key Features"

    def __str__(self):
        return self.short_description

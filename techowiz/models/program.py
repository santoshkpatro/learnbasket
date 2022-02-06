from django.db import models
from techowiz.models.base import BaseModel
from techowiz.models.category import Category


class AvailableProgramManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_public=True)


class Program(BaseModel):
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='parent_programs'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='category_programs'
    )
    thumbnail = models.URLField(blank=True, null=True)
    intro = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=350, unique=True)
    duration_in_days = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    syllabus = models.JSONField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    is_free = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    available_objects = AvailableProgramManager()

    class Meta:
        db_table = 'programs'

    def __str__(self) -> str:
        return self.title
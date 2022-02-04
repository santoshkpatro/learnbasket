from django.db import models
from core.models.base import BaseModel
from core.models.category import Category


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

    class Meta:
        db_table = 'programs'

    def __str__(self) -> str:
        return self.slug
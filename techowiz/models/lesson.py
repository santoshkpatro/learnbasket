from django.db import models
from techowiz.models.base import BaseModel
from techowiz.models.program import Program


class Lesson(BaseModel):
    sl = models.PositiveIntegerField(blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    resource = models.URLField(blank=True, null=True)
    assignment = models.URLField(blank=True, null=True)
    video_src = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'lessons'

    def __str__(self) -> str:
        return self.title

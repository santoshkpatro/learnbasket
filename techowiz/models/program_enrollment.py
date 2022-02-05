from django.db import models
from techowiz.models.base import BaseModel
from techowiz.models.user import User
from techowiz.models.program import Program


class ProgramEnrollment(BaseModel):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_enrollments'
    )
    program = models.ForeignKey(
        Program, 
        on_delete=models.CASCADE, 
        related_name='program_enrollments'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'program_enrollments'
        unique_together = ['user', 'program']
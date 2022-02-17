from django.db import models
from server.models.base import BaseModel
from server.models.user import User
from server.models.program import Program


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

    def __str__(self) -> str:
        return str(self.id)
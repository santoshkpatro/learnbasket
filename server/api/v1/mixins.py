from rest_framework import status
from rest_framework.exceptions import APIException
from server.models import Program


class EnrollmentException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'You are not enrolled in this program'


class ProgramException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Program not found'


class ProgramEnrolledMixin:
    def get_program(self):
        program_id = self.kwargs['program_id']
        try:
            program = Program.available_objects.get(id=program_id)
            enrolled_programs = Program.objects.filter(
                program_enrollments__user=self.request.user, 
                program_enrollments__is_active=True
            )

            if not program in enrolled_programs:
                raise EnrollmentException

            return program
        except Program.DoesNotExist:
            raise ProgramException
from rest_framework import generics, permissions
from techowiz.api.v1.programs.serializers import ProgramSerializer, ProgramDetailSerializer, LessonSerializer
from techowiz.models.program import Program
from techowiz.models.lesson import Lesson
from techowiz.api.v1.mixins import ProgramEnrolledMixin
from techowiz.api.v1.permissions import IsMaintainer


class ProgramListView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    queryset = Program.available_objects.filter(parent=None)


class ProgramDetailView(generics.RetrieveAPIView):
    serializer_class = ProgramDetailSerializer
    queryset = Program.available_objects.filter(parent=None)


class ProgramEnrolledView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    queryset = Program.available_objects.all()
    permission_classes = [permissions.IsAuthenticated, IsMaintainer]

    def get_queryset(self):
        return super().get_queryset().filter(
            program_enrollments__user=self.request.user, 
            program_enrollments__is_active=True
        )


class LessonListView(generics.ListAPIView, ProgramEnrolledMixin):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        program = self.get_program()
        return super().get_queryset().filter(program=program).order_by('sl')


class LessonCreateView(generics.CreateAPIView, ProgramEnrolledMixin):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        program = self.get_program()
        lesson = serializer.save(program=program)
        return lesson
from rest_framework import generics, permissions, status
from techowiz.api.v1.programs.serializers import ProgramSerializer, ProgramDetailSerializer
from techowiz.models.program import Program


class ProgramListView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    queryset = Program.available_objects.filter(parent=None)


class ProgramDetailView(generics.RetrieveAPIView):
    serializer_class = ProgramDetailSerializer
    queryset = Program.available_objects.filter(parent=None)


class ProgramEnrolledView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    queryset = Program.available_objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(
            program_enrollments__user=self.request.user, 
            program_enrollments__is_active=True
        )

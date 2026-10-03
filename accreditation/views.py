from django.db import transaction

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accreditation.models import Assessment, Criterion
from accreditation.serializers import AssessmentSerializer


NBA_CRITERIA = [
    (1, "Outcome-Based Curriculum", 120),
    (2, "Outcome-Based Teaching Learning", 120),
    (3, "Outcome-Based Assessment", 120),
    (4, "Students' Performance", 120),
    (5, "Faculty Information", 100),
    (6, "Faculty Contributions", 120),
    (7, "Facilities and Technical Support", 100),
    (8, "Continuous Improvement", 80),
    (9, "Student Support and Governance", 120),
]


class AssessmentCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        assessments = Assessment.objects.all().order_by("-created_at")

        serializer = AssessmentSerializer(
            assessments,
            many=True
        )

        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):

        serializer = AssessmentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        assessment = serializer.save(
            created_by=request.user
        )

        Criterion.objects.bulk_create([
            Criterion(
                assessment=assessment,
                number=number,
                name=name,
                maximum_marks=marks,
            )
            for number, name, marks in NBA_CRITERIA
        ])

        return Response(
            AssessmentSerializer(assessment).data,
            status=status.HTTP_201_CREATED
        )
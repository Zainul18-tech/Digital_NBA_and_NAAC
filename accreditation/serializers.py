from rest_framework import serializers

from accreditation.models import Assessment


class AssessmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assessment
        fields = [
            "id",
            "program",
            "academic_year",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        ]
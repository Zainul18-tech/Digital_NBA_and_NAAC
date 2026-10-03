from django.urls import path

from accreditation.views import AssessmentCreateView


urlpatterns = [
    path(
        "assessments/",
        AssessmentCreateView.as_view(),
        name="assessment-create"
    ),
]
from django.conf import settings
from django.db import models


class Assessment(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        CLOSED = "CLOSED", "Closed"

    program = models.ForeignKey(
        "core.Program",
        on_delete=models.CASCADE,
        related_name="assessments"
    )

    academic_year = models.ForeignKey(
        "core.AcademicYear",
        on_delete=models.PROTECT,
        related_name="assessments"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_assessments"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["program", "academic_year"],
                name="unique_program_academic_year_assessment"
            )
        ]

    def __str__(self):
        return f"{self.program} - {self.academic_year}"


class Criterion(models.Model):

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="criteria"
    )

    number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    maximum_marks = models.PositiveIntegerField()

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(
                fields=["assessment", "number"],
                name="unique_assessment_criterion_number"
            )
        ]

    def __str__(self):
        return f"Criterion {self.number} - {self.name}"


class SubCriterion(models.Model):

    criterion = models.ForeignKey(
        Criterion,
        on_delete=models.CASCADE,
        related_name="subcriteria"
    )

    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    maximum_marks = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["criterion", "code"],
                name="unique_criterion_subcriterion_code"
            )
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

# PEO MODEL

class PEO(models.Model):

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="peos"
    )

    code = models.CharField(max_length=20)
    statement = models.TextField()

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["assessment", "code"],
                name="unique_assessment_peo_code"
            )
        ]

    def __str__(self):
        return f"{self.code} - {self.statement[:50]}"

# VISION MODEL

class VisionMission(models.Model):

    assessment = models.OneToOneField(
        Assessment,
        on_delete=models.CASCADE,
        related_name="vision_mission"
    )

    institute_vision = models.TextField()
    institute_mission = models.TextField()

    department_vision = models.TextField()
    department_mission = models.TextField()

    def __str__(self):
        return f"Vision & Mission - {self.assessment}"


# MissionPEOMapping Model

class MissionPEOMapping(models.Model):

    class CorrelationLevel(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    peo = models.ForeignKey(
        PEO,
        on_delete=models.CASCADE,
        related_name="mission_mappings"
    )

    mission_element = models.CharField(max_length=255)

    correlation_level = models.PositiveSmallIntegerField(
        choices=CorrelationLevel.choices,
        null=True,
        blank=True
    )

    justification = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["peo", "mission_element"],
                name="unique_peo_mission_element"
            )
        ]

    def __str__(self):
        return f"{self.peo.code} - {self.mission_element}"


# CurriculumCourse Model

class CurriculumCourse(models.Model):

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="curriculum_courses"
    )

    course_code = models.CharField(max_length=50)
    course_title = models.CharField(max_length=255)

    classroom_instruction_hours = models.PositiveIntegerField(default=0)
    laboratory_instruction_hours = models.PositiveIntegerField(default=0)
    term_work_hours = models.PositiveIntegerField(default=0)
    self_learning_hours = models.PositiveIntegerField(default=0)

    total_hours = models.PositiveIntegerField(default=0)
    total_credits = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = ["course_code"]
        constraints = [
            models.UniqueConstraint(
                fields=["assessment", "course_code"],
                name="unique_assessment_course_code"
            )
        ]

    def __str__(self):
        return f"{self.course_code} - {self.course_title}"

# CurriculumComponent Model

class CurriculumComponent(models.Model):

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="curriculum_components"
    )

    name = models.CharField(max_length=255)

    credit_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    contact_hours = models.PositiveIntegerField(default=0)

    total_credits = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["assessment", "name"],
                name="unique_assessment_curriculum_component"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.assessment}"
    

# CurriculumGapAnalysis Model

class CurriculumGapAnalysis(models.Model):

    assessment = models.OneToOneField(
        Assessment,
        on_delete=models.CASCADE,
        related_name="curriculum_gap_analysis"
    )

    process_description = models.TextField()

    identified_gaps = models.TextField(
        blank=True
    )

    all_pos_met = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = "Curriculum Gap Analysis"
        verbose_name_plural = "Curriculum Gap Analyses"

    def __str__(self):
        return f"Curriculum Gap Analysis - {self.assessment}"
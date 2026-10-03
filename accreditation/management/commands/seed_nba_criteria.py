from django.core.management.base import BaseCommand, CommandError

from accreditation.models import Assessment, Criterion


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


class Command(BaseCommand):

    help = "Create the 9 NBA Tier-II criteria for an assessment"

    def add_arguments(self, parser):
        parser.add_argument(
            "assessment_id",
            type=int,
            help="ID of the assessment"
        )

    def handle(self, *args, **options):

        assessment_id = options["assessment_id"]

        try:
            assessment = Assessment.objects.get(id=assessment_id)
        except Assessment.DoesNotExist:
            raise CommandError(
                f"Assessment with ID {assessment_id} does not exist."
            )

        created_count = 0

        for number, name, marks in NBA_CRITERIA:

            _, created = Criterion.objects.get_or_create(
                assessment=assessment,
                number=number,
                defaults={
                    "name": name,
                    "maximum_marks": marks,
                }
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{created_count} NBA criteria created for Assessment "
                f"{assessment_id}."
            )
        )
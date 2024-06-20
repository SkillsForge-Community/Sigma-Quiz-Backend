from factory.django import DjangoModelFactory

from sigma.school.models import School


class SchoolFactory(DjangoModelFactory):
    class Meta:
        model = School

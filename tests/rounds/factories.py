from factory.django import DjangoModelFactory

from sigma.round.models import Round


class RoundFactory(DjangoModelFactory):
    class Meta:
        model = Round

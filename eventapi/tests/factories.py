from django.utils import timezone
import factory
from factory import fuzzy

from ..models import Event


CATEGORIES = ('page interaction', 'form interaction')
NAMES = ('submit', 'pageview', 'click')


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    session_id = factory.Faker('md5', raw_output=False)
    category = factory.fuzzy.FuzzyChoice(CATEGORIES)
    name = factory.fuzzy.FuzzyChoice(NAMES)
    data = factory.Sequence(
        lambda n: {'host': f'www.consumerreports{n}.com', 'path': '/'}
    )
    timestamp = factory.Faker(
        'date_time_this_year', before_now=True, tzinfo=timezone.get_current_timezone()
    )

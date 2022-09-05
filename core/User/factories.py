import factory
from factory import faker, fuzzy
from .models import User


class UserFactory(factory.DjangoModelFactory):
    username = fuzzy.FuzzyText(length=20)
    email = faker.Faker('email')

    first_name = fuzzy.FuzzyText(length=20)
    last_name = fuzzy.FuzzyText(length=20)
    middle_name = fuzzy.FuzzyText(length=20)

    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = User

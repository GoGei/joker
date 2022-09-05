from factory import faker, SubFactory, DjangoModelFactory
from .models import PrivilegeUser, PrivilegeMessage


class PrivilegeUserFactory(DjangoModelFactory):
    class Meta:
        model = PrivilegeUser

    user = SubFactory('core.User.factories.UserFactory')


class PrivilegeMessageFactory(DjangoModelFactory):
    class Meta:
        model = PrivilegeMessage

    privilege_user = SubFactory(PrivilegeUserFactory)
    message = faker.Faker('paragraph', nb_sentences=5)

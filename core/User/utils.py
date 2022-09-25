import time
from django.utils import timezone
from django.core.cache import cache
from django_hosts.resolvers import reverse as host_reverse


class RegistrationCodeHandler(object):
    KEY_PATTERN = 'user_registration_code_%s'

    def __init__(self, user, request=None):
        self.user = user
        self.expire_time = user.REGISTRATION_CODE_EXPIRE_TIME_SECONDS
        self.request = request

    def clean_previous(self):
        key = self.KEY_PATTERN % self.user.id
        cache.delete(key)

    def create_registration_code(self):
        user = self.user
        code = self.user.hashid().encode(int(time.time()), user.id)

        self.clean_previous()

        key = self.KEY_PATTERN % user.id
        value = code
        timeout = self.expire_time
        cache.set(key, value, timeout=timeout)

        return code

    def generate_activation_link(self):
        code = self.create_registration_code()
        link = host_reverse('home-register-activate', host='public', args=[self.user.id, code])
        if self.request:
            link = self.request.build_absolute_uri(link)
        return link

    def validate_registration_code(self, code):
        user = self.user
        try:
            stamp, user_id = user.hashid().decode(code)
        except ValueError:
            raise ValueError('Code is not valid')

        if user_id != user.pk:
            raise ValueError('Got incorrect user by this code')

        now = timezone.now()
        stamp = timezone.datetime.fromtimestamp(stamp, tz=now.tzinfo)
        expire_date = now - timezone.timedelta(seconds=self.expire_time)
        if stamp < expire_date:
            raise ValueError('Code is expired')

        return user

def manager_check(u):
    if not u:
        return False
    return u.is_active and u.is_staff or u.is_superuser


def superuser_check(u):
    return manager_check(u) and u.is_superuser

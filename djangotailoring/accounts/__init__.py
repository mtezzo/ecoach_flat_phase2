def account_setup_complete(user):
    return user.email and user.has_usable_password()


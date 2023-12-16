from authentication.signals import user_created, otp_created


def custom_user_created_handler(sender, token, **kwargs):
    """we will receive a token here that needs to be sent to the user"""
    print(token)


def custom_otp_created_handler(sender, instance, **kwargs):
    """we will receive a otp here"""
    print(instance)


user_created.connect(custom_user_created_handler)
otp_created.connect(custom_otp_created_handler)

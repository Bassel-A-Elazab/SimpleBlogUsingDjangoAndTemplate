from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin)
        try:
            name = sociallogin.account.extra_data["name"]
            print("here")
            user.name = name
            user.save()
        except (KeyError, AttributeError):
            pass
        return user

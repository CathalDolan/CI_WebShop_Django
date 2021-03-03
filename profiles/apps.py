from django.apps import AppConfig, render


class ProfilesConfig(AppConfig):
    name = 'profiles'


def profiles(request):
        return render(request, 'profiles.html')

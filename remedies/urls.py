from django.urls import path
from .views import home, vedabot_api, remedies_page

urlpatterns = [
    path("", home, name="home"),
    path("vedabot/", vedabot_api, name="vedabot"),
    path("remedies/", remedies_page, name="remedies"),
]


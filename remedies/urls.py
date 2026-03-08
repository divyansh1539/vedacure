from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("services/", services, name="services"),
    path("ai/", ai_suggest, name="ai_suggest"),
    path("about/", about, name="about"),
    path("blog/", blog, name="blog"),
    path("contact/", contact, name="contact"),

    # Category Page (Haircare, Skincare etc.)
    path("category/<slug:slug>/", category_detail, name="category_detail"),

    # ⭐ Problem Detail Page (Hair Fall → Remedies page)
    path("problem/<str:name>/", problem_detail, name="problem_detail"),

    # VedaBOT API
    path("vedabot/", vedabot_api, name="vedabot_api"),
]
from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("remedies/", remedies_page, name="remedies"),
    path("ai/", ai_suggest, name="ai_suggest"),
    path("about/", about, name="about"),
    path("blog/", blog, name="blog"),
    path("contact/", contact, name="contact"),
]



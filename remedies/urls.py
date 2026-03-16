from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ================= AUTHENTICATION =================
    path("login/", login_page, name="login"),
    path("signup/", signup_page, name="signup"),
    path("logout/", logout_user, name="logout"),
    
    # ================= PASSWORD RESET =================
    # ================= PASSWORD RESET =================

path("password-reset/", auth_views.PasswordResetView.as_view(
    template_name="password_reset.html",
    email_template_name="password_reset_email.html",
    subject_template_name="password_reset_subject.txt"
), name="password_reset"),

path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
    template_name="password_reset_done.html"
), name="password_reset_done"),

path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
    template_name="password_reset_confirm.html"
), name="password_reset_confirm"),

path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
    template_name="password_reset_complete.html"
), name="password_reset_complete"),
    
    # ================= EXISTING ROUTES =================
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from profilepage import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls"), name="home"),
    path("profilepage/", include("profilepage.urls"), name="profile"),
    path("chat/", include("chat.urls"), name="chat"),
    # password reset
    path(
        "reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # google
    path("accounts/", include("allauth.urls")),
    # captcha
    path("captcha/", include("captcha.urls")),
    # ckeditor
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # paypal
    path("paypal/", include("paypal.standard.ipn.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

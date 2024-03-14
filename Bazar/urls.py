from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from profilepage import views

from django.contrib.auth import views as auth_views

# ckeditor
from ckeditor_uploader import views as ckeditor_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

urlpatterns = [
    # path to the admin page
    path("admin/", admin.site.urls),
    # path to the homepage
    path("", include("homepage.urls"), name="home"),
    # path to the profile page
    path("profilepage/", include("profilepage.urls"), name="profile"),
    # path to the chat page
    path("chat/", include("chat.urls"), name="chat"),
    # google
    path("accounts/", include("allauth.urls")),
    # captcha
    path("captcha/", include("captcha.urls")),
    # ckeditor
    path("ckeditor/upload/", login_required(ckeditor_views.upload), name="ckeditor_upload"),
    path("ckeditor/browse/", never_cache(login_required(ckeditor_views.browse)), name="ckeditor_browse"),
    # paypal
    path("paypal/", include("paypal.standard.ipn.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # this is for the media files

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

#store files path in db and file in disk, future scope=move to S3
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

#This is the root URL configuration. It routes /admin/ to the admin site and everything else to our core app, and in development mode it also serves uploaded PDF files from the media folder.
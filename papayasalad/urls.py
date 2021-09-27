from django.contrib import admin
from django.urls import include, path
from papayasalad import views as core_views
from django import views as django_views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('practice/', include('practice.urls')),
    path('admin/', admin.site.urls),
	path('accounts/signup/', core_views.signup),
	path('accounts/signout/', core_views.signout),
	path('', core_views.index),
	path('accounts/', include('django.contrib.auth.urls')),
	path('quizzes/', include('quizzes.urls')),
	path('vocab/', include('vocab.urls')),
	path('media/', django_views.static.serve),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from commerce.views import health_check, attack_test_view, attack_test_query, metrics_view, platform_identity

urlpatterns = [
    path('admin/',                          admin.site.urls),
    path('',                                include('commerce.urls')),
    path('accounts/',                       include('allauth.urls')),
    path('silk/',                           include('silk.urls', namespace='silk')),
    path('health/',                         health_check,       name='health'),
    path('metrics/',                        metrics_view,       name='metrics'),
    path('debug/identity/',                 platform_identity,  name='platform_identity'),
    path('attack-test/',                    attack_test_query,  name='attack_test'),
    path('attack-test/<path:payload>',      attack_test_view,   name='attack_test_payload'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
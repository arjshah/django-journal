from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')), # include() function includes the default auth urls
    path('', include('learning_logs.urls')),

]

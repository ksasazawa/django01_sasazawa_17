from django.contrib import admin
from django.urls import path
from chat_app.views import frontpage, check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name="frontpage"),
    path('check/', check, name="check"),
]


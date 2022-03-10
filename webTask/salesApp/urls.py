import threading
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

IsDoingEveryMonth = False

urlpatterns = [
    # get Api.
    path('getTopItems/', views.get_top_items),
    path('getItems/', views.getItems),
    path('getReceipts/', views.getReceipts),
    # set and add Api.
    path('addReceipt/', views.addReceipt),
    path('addItem/', views.addItem),
    # edit and add Api.
    path('editReceipt/', views.editReceipt),
    path('editItem/', views.editItems),
    # user management Api.
    path('login/', views.log_in),
    path('logout/', views.logout_user),
    path('signup/', views.signup),
    path('get_me/', views.get_me),
    # delete Api.
    path('deleteItem/', views.deleteItem),

    path('test/', views.test),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)

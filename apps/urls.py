from django.urls import path
from .views import index, login, register, dashboard, new_trip, edit_trip, cancel, join, detail, remove,logout


urlpatterns = [
    path('', index),
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('dashboard/', dashboard),
    path('new-trip/', new_trip),
    path('detail-trip/<int:id>/', detail),
    path('edit-trip/<int:id>/', edit_trip),
    path('cancel-trip/<int:id>/', cancel),
    path('join-trip/<int:id>/', join),
    path('delete-trip/<int:id>/', remove),
]

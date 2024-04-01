from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.landing, name="landing"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("car-page/", views.car_page, name="car-page"),
    path("reserver/<str:pk>/", views.reserver, name="reserver"),
    path("confirmer/<str:pk>/", views.confirmer, name="confirmer"),
    path("reserver/<str:pk>/login", views.res_login, name="res-login"),
    path("reserver/<str:pk>/sign-up", views.res_register, name="res-register"),
    path("car-info/<str:pk>/", views.car_info, name="car-info"),
    path("profile/", views.profil, name="profil"),
    path("avis/", views.add_review, name="avis"),
    path("avis/login", views.rev_login, name="rev-login"),
    path("avis/sign-up", views.rev_register, name="rev-register"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("cars/", views.cars, name="cars"),
    path("add-car/", views.add_car, name="add-car"),
    path("edit-car/<str:pk>/", views.edit_car, name="edit-car"),
    path("delete-car/<str:pk>/", views.delete_car, name="delete-car"),
    path("reservation/", views.reservation, name="reservation"),
    path("users/", views.users, name="users"),
    path("edit-user/<str:pk>/", views.edit_user, name="edit-user"),
    path("delete-user/<str:pk>/", views.delete_user, name="delete-user"),
    path("reviews/", views.reviews, name="reviews"),
    path("logs/", views.logs, name="logs"),

  
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
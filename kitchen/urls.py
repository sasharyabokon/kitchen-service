from django.urls import path

from kitchen.views import (
    index,
    DishTypeListView,
    DishListView,
    CookListView,
    DishTypeDetailView,
    CookDetailView,
    DishDetailView,

)

urlpatterns = [
    path("",index, name="index"),
    path("dish-type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("cooks/", CookListView.as_view(), name="cooks-list"),
    path("dish-type/<int:pk>/", DishTypeDetailView.as_view(), name="dish-type-detail"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cooks-detail"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),

]

app_name = "kitchen"
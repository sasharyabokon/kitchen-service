from django.urls import path

from kitchen.views import (
    index,
    DishTypeListView,
    DishListView,
    CookListView,
    DishTypeDetailView,
    CookDetailView,

)

urlpatterns = [
    path("",index, name="index"),
    path("dish_type/", DishTypeListView.as_view(), name="dish_type_list"),
    path("dish/", DishListView.as_view(), name="dish_list"),
    path("cooks/", CookListView.as_view(), name="cooks_list"),
    path("dish_type/<int:pk>/", DishTypeDetailView.as_view(), name="dish_type_detail"),
    path("cooks/<int:pk>", CookDetailView.as_view(), name="cooks_detail"),

]

app_name = "kitchen"
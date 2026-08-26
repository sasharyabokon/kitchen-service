from django.urls import path

from kitchen.views import (
    index,
    DishTypeListView,
    DishListView,
    CookListView,
    DishTypeDetailView,
    CookDetailView,
    DishDetailView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,

)

urlpatterns = [
    path("",index, name="index"),
    path("dish-type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-type/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish-type/update/<int:pk>/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish-type/delete/<int:pk>/", DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("dish/create/", DishCreateView.as_view(), name="dish-create"),
    path("dish/update/<int:pk>/", DishUpdateView.as_view(), name="dish-update"),
    path("dish/delete/<int:pk>/", DishDeleteView.as_view(), name="dish-delete"),
    path("cooks/", CookListView.as_view(), name="cooks-list"),
    path("cooks/create/", CookCreateView.as_view(), name="cooks-create"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/update/<int:pk>/", CookUpdateView.as_view(), name="cook-update"),
    path("cooks/delete/<int:pk>/", CookDeleteView.as_view(), name="cook-delete"),
    path("dish-type/<int:pk>/", DishTypeDetailView.as_view(), name="dish-type-detail"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cooks-detail"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),


]

app_name = "kitchen"
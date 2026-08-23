from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView

from kitchen.models import Dish, DishType, Cook


def index(request: HttpRequest) -> HttpResponse:
    num_dish = Dish.objects.count()
    num_dish_types = DishType.objects.count()
    num_cooks = Cook.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_dish": num_dish,
        "num_dish_types": num_dish_types,
        "num_cooks": num_cooks,
        "num_visits": num_visits + 1,
    }
    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"


class DishTypeDetailView(DetailView):
    model = DishType
    template_name = "kitchen/dish_type_detail.html"
    context_object_name = "dish_type"



class DishListView(ListView):
    model = Dish
    paginate_by = 10
    queryset = Dish.objects.all().select_related("dish_type")
    context_object_name = "dishes"

class DishDetailView(DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"
    context_object_name = "dish"


class CookListView(ListView):
    model = Cook
    paginate_by = 10
    template_name = "kitchen/cooks_list.html"
    context_object_name = "cooks"


class CookDetailView(DetailView):
    model = Cook
    template_name = "kitchen/cooks_detail.html"
    context_object_name = "cook"

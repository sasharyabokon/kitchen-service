from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView

from kitchen.models import Dish, DishType, Cook


@login_required
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


class DishTypeListView(LoginRequiredMixin, ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"


class DishTypeDetailView(LoginRequiredMixin, DetailView):
    model = DishType
    template_name = "kitchen/dish_type_detail.html"
    context_object_name = "dish_type"



class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    paginate_by = 10
    queryset = Dish.objects.all().select_related("dish_type")
    context_object_name = "dishes"

class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"
    context_object_name = "dish"


class CookListView(LoginRequiredMixin, ListView):
    model = Cook
    paginate_by = 10
    template_name = "kitchen/cooks_list.html"
    context_object_name = "cooks"


class CookDetailView(LoginRequiredMixin, DetailView):
    model = Cook
    template_name = "kitchen/cooks_detail.html"
    context_object_name = "cook"

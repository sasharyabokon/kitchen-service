from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView

from kitchen.forms import (CookCreationForm,
                           DishForm,
                           CookUpdateForm,
                           DishSearchForm,
                           IngredientSearchForm
                           )
from kitchen.models import Dish, DishType, Cook, Ingredient


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_dish = Dish.objects.count()
    num_dish_types = DishType.objects.count()
    num_cooks = Cook.objects.count()
    num_ingredients = Ingredient.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_dish": num_dish,
        "num_dish_types": num_dish_types,
        "num_cooks": num_cooks,
        "num_ingredients": num_ingredients,
        "num_visits": num_visits + 1,
    }
    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "kitchen/dish_type_detail.html"
    context_object_name = "dish_type"


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Dish type successfully created!")
        return response


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Dish type successfully updated!")
        return response


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_confirm_delete.html"

    def form_valid(self, form):
        success_url = self.get_success_url()
        messages.success(self.request, "Dish type successfully deleted!")
        self.object.delete()
        return HttpResponseRedirect(success_url)


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    paginate_by = 10
    queryset = Dish.objects.select_related("dish_type")
    context_object_name = "dishes"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Dish successfully created!")
        return response


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Dish successfully updated!")
        return response


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")
    template_name = "kitchen/dish_confirm_delete.html"

    def form_valid(self, form):
        success_url = self.get_success_url()
        messages.success(self.request, "Dish successfully deleted!")
        self.object.delete()
        return HttpResponseRedirect(success_url)


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"
    context_object_name = "dish"


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 10
    template_name = "kitchen/cooks_list.html"
    context_object_name = "cooks"

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cooks-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cook successfully created!")
        return response


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    template_name = "kitchen/cooks_detail.html"
    context_object_name = "cook"


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cooks-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cook successfully updated!")
        return response


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cooks-list")
    template_name = "kitchen/cook_confirm_delete.html"

    def form_valid(self, form):
        success_url = self.get_success_url()
        messages.success(self.request, "Cook successfully deleted!")
        self.object.delete()
        return HttpResponseRedirect(success_url)


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    paginate_by = 10
    success_url = reverse_lazy("kitchen:ingredient-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IngredientListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Ingredient.objects.prefetch_related("dishes")
        form = IngredientSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")
    template_name = "kitchen/ingredient_form.html"
    fields = "__all__"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Ingredient successfully created!")
        return response


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")
    template_name = "kitchen/ingredient_form.html"
    fields = "__all__"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Ingredient successfully updated!")
        return response


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")
    template_name = "kitchen/ingredient_confirm_delete.html"

    def form_valid(self, form):
        success_url = self.get_success_url()
        messages.success(self.request, "Ingredient successfully deleted!")
        self.object.delete()
        return HttpResponseRedirect(success_url)

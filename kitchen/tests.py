from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import Dish, Ingredient, DishType, Cook

User = get_user_model()


class DishSearchTests(TestCase):
    def setUp(self):
        self.user = (User.objects.create_user
                     (username="roma",
                      password="112322d")
                     )
        self.client.login(username="roma", password="112322d")
        self.dish_type = DishType.objects.create(name="Dessert")
        self.ingredient = Ingredient.objects.create(name="Apple")
        self.dish1 = Dish.objects.create(
            name="Apple Pie",
            description="Pie",
            price=170,
            dish_type=self.dish_type
        )
        self.dish1.ingredients.add(self.ingredient)
        self.dish2 = Dish.objects.create(
            name="Banana Cake",
            description="Cake",
            price=200,
            dish_type=self.dish_type
        )

    def test_dish_list_without_search(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apple Pie")
        self.assertContains(response, "Banana Cake")

    def test_dish_list_with_search(self):
        response = self.client.get(
            reverse("kitchen:dish-list"), {"name": "Apple"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apple Pie")
        self.assertNotContains(response, "Banana Cake")

    def test_dish_detail_shows_ingredients(self):
        url = reverse("kitchen:dish-detail", args=[self.dish1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apple Pie")
        self.assertContains(response, "Apple")


class IngredientSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="roma",
            password="112322d"
        )
        self.client.login(username="roma", password="112322d")
        self.ingredient1 = Ingredient.objects.create(name="Apple")
        self.ingredient2 = Ingredient.objects.create(name="Banana")

    def test_ingredient_list_without_search(self):
        response = self.client.get(
            reverse("kitchen:ingredient-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apple")
        self.assertContains(response, "Banana")

    def test_ingredient_list_with_search(self):
        response = self.client.get(
            reverse("kitchen:ingredient-list"), {"name": "Apple"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apple")
        self.assertNotContains(response, "Banana")


class CookSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="roma",
            password="112322d"
        )
        self.client.login(
            username="roma",
            password="112322d"
        )
        self.cook1 = Cook.objects.create(
            username="chef1",
            years_of_experience=5
        )
        self.cook2 = Cook.objects.create(
            username="chef2",
            years_of_experience=10
        )

    def test_cook_list_without_search(self):
        response = self.client.get(reverse("kitchen:cooks-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "chef1")
        self.assertContains(response, "chef2")

    def test_cook_list_with_search(self):
        response = self.client.get(
            reverse(
                "kitchen:cooks-list"), {"username": "chef1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "chef1")
        self.assertNotContains(response, "chef2")

    def test_cooks_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("kitchen:cooks-list"))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn("/accounts/login/", response.url)


class DishTypeSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="roma",
            password="112322d"
        )
        self.client.login(username="roma", password="112322d")
        self.type1 = DishType.objects.create(name="Dessert")
        self.type2 = DishType.objects.create(name="Main Course")

    def test_dishtype_list_without_search(self):
        response = self.client.get(reverse("kitchen:dish-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dessert")
        self.assertContains(response, "Main Course")

    def test_dishtype_list_with_search(self):
        response = self.client.get(
            reverse("kitchen:dish-type-list"), {"name": "Dessert"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dessert")
        self.assertNotContains(response, "Main Course")

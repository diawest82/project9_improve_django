from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Menu, Item, Ingredient

menu_data1 = {
    "season": 'Summer Menu',
    "expiration_date": '2017-09-15'
}

menu_data2 = {
    "season": "Fall Menu",
    "expiration_date": "2017-11-21"
}


class TestInfo(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            username='test_user',
            email='testemail@gmail.com',
            password='test_pass'
        )

        ingredient1 = Ingredient(name='strawberry')
        ingredient1.save()
        ingredient2 = Ingredient(name='chocolate')
        ingredient2.save()
        self.items = Item(
            id=5,
            name='strawberry soda',
            description='delicious',
            chef=self.test_user
        )
        self.items.save()
        self.items.ingredients.add(ingredient2, ingredient1)
        self.menu1 = Menu.objects.create(**menu_data1)
        self.menu2 = Menu.objects.create(**menu_data2)
        self.menu1.items.add(self.items)
        self.menu2.items.add(self.items)


class MenuViewsTest(TestInfo):
    def test_list_all_current_menu_view(self):
        resp = self.client.get(reverse("menu:menu_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu1, resp.context['menus'])
        self.assertIn(self.menu2, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu1.season)

    def test_menu_detail_view(self):
        resp = self.client.get(reverse("menu:menu_detail",
                                       kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu1, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_menu_detail_404(self):
        resp = self.client.get(reverse("menu:menu_detail",
                                       kwargs={'pk': 5}))
        self.assertEqual(resp.status_code, 404)

    def test_item_list_view(self):
        resp = self.client.get(reverse('menu:item_detail',
                                       kwargs={'pk': self.items.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.items, resp.context['item'])
        self.assertTemplateUsed(resp, 'menu/detail_item.html')

    def test_item_list_404(self):
        resp = self.client.get(reverse('menu:item_detail',
                                       kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 404)

    def test_change_menu_view(self):
        resp = self.client.get(reverse('menu:menu_edit',
                                       kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu1, resp.context['menu'])
        self.assertIn(self.items, resp.context['items'])
        self.assertTemplateUsed(resp, 'menu/change_menu.html')

    def test_create_new_menu_view_GET(self):
        resp = self.client.get(reverse('menu:new_menu',))
        self.assertEqual(resp.status_code, 200)


class MenuModelTest(TestCase):
    def test_create_menu(self):
        menu = Menu.objects.create(**menu_data2)
        self.assertEqual(menu.season, 'Fall Menu')

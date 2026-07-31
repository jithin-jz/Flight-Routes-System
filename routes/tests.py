from django.test import TestCase, Client
from django.urls import reverse
from .models import Airport
from .forms import AddAirportForm


class AirportModelTest(TestCase):
    def test_create_airport_and_str(self):
        root = Airport.objects.create(code="JFK", duration=120)
        self.assertEqual(str(root), "JFK")
        self.assertIsNone(root.left)
        self.assertIsNone(root.right)

    def test_tree_relationships(self):
        root = Airport.objects.create(code="JFK", duration=120)
        left_child = Airport.objects.create(code="ORD", duration=90)
        right_child = Airport.objects.create(code="LAX", duration=300)

        root.left = left_child
        root.right = right_child
        root.save()

        self.assertEqual(root.left.code, "ORD")
        self.assertEqual(root.right.code, "LAX")


class AddAirportFormTest(TestCase):
    def test_valid_root_airport(self):
        form = AddAirportForm(
            data={"parent": "", "position": "", "code": "del", "duration": 150}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["code"], "DEL")

    def test_valid_child_airport(self):
        root = Airport.objects.create(code="JFK", duration=120)
        form = AddAirportForm(
            data={"parent": root.id, "position": "left", "code": "BOS", "duration": 45}
        )
        self.assertTrue(form.is_valid())

    def test_missing_position_when_parent_selected(self):
        root = Airport.objects.create(code="JFK", duration=120)
        form = AddAirportForm(
            data={"parent": root.id, "position": "", "code": "BOS", "duration": 45}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Please select a position", form.non_field_errors()[0])

    def test_position_selected_without_parent(self):
        form = AddAirportForm(
            data={"parent": "", "position": "left", "code": "BOS", "duration": 45}
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Position should not be selected if no parent is chosen",
            form.non_field_errors()[0],
        )

    def test_duplicate_airport_code(self):
        Airport.objects.create(code="JFK", duration=120)
        form = AddAirportForm(
            data={"parent": "", "position": "", "code": "JFK", "duration": 60}
        )
        self.assertFalse(form.is_valid())

    def test_occupied_child_position(self):
        root = Airport.objects.create(code="JFK", duration=120)
        left = Airport.objects.create(code="ORD", duration=90)
        root.left = left
        root.save()

        form = AddAirportForm(
            data={"parent": root.id, "position": "left", "code": "SFO", "duration": 200}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("already has a left child", form.non_field_errors()[0])


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "routes/home.html")

    def test_add_airport_view_get(self):
        response = self.client.get(reverse("add_airport"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "routes/add_airport.html")

    def test_add_airport_view_post_success(self):
        response = self.client.post(
            reverse("add_airport"),
            {"parent": "", "position": "", "code": "DXB", "duration": 240},
        )
        self.assertRedirects(response, reverse("add_airport"))
        self.assertTrue(Airport.objects.filter(code="DXB").exists())

    def test_search_airport_view_left_traversal(self):
        root = Airport.objects.create(code="A", duration=100)
        b = Airport.objects.create(code="B", duration=80)
        c = Airport.objects.create(code="C", duration=60)
        root.left = b
        root.save()
        b.left = c
        b.save()

        response = self.client.post(
            reverse("search"), {"start_airport": root.id, "direction": "left"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "routes/search.html")
        self.assertEqual(response.context["result"], c)

    def test_search_airport_view_right_traversal(self):
        root = Airport.objects.create(code="A", duration=100)
        r1 = Airport.objects.create(code="R1", duration=120)
        root.right = r1
        root.save()

        response = self.client.post(
            reverse("search"), {"start_airport": root.id, "direction": "right"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result"], r1)

    def test_longest_duration_view(self):
        Airport.objects.create(code="SHORT", duration=30)
        Airport.objects.create(code="LONG", duration=500)
        Airport.objects.create(code="MID", duration=150)

        response = self.client.get(reverse("longest"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "routes/longest.html")
        self.assertEqual(response.context["airport"].code, "LONG")

    def test_shortest_duration_view(self):
        Airport.objects.create(code="SHORT", duration=30)
        Airport.objects.create(code="LONG", duration=500)

        response = self.client.get(reverse("shortest"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "routes/shortest.html")
        self.assertEqual(response.context["airport"].code, "SHORT")

    def test_home_post_add_airport(self):
        response = self.client.post(
            reverse("home"),
            {
                "form_type": "add_airport",
                "parent": "",
                "position": "",
                "code": "SYD",
                "duration": 300,
            },
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(Airport.objects.filter(code="SYD").exists())

    def test_home_post_search_airport(self):
        root = Airport.objects.create(code="JFK", duration=100)
        left = Airport.objects.create(code="ORD", duration=80)
        root.left = left
        root.save()

        response = self.client.post(
            reverse("home"),
            {
                "form_type": "search_airport",
                "start_airport": root.id,
                "direction": "left",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["search_result"], left)
        self.assertIn("JFK", response.content.decode())
        self.assertIn("ORD", response.content.decode())

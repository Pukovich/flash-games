from django.test import TestCase
from .models import YourModel

class YourModelTestCase(TestCase):
    def setUp(self):
        # Создание тестовых данных
        YourModel.objects.create(name="Test Name")

    def test_model_name(self):
        # Проверка корректности данных
        obj = YourModel.objects.get(name="Test Name")
        self.assertEqual(obj.name, "Test Name")
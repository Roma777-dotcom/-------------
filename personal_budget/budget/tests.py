from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Operation
from django.utils import timezone

class BudgetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(
            user=self.user,
            name='Еда',
            type='expense',
            color='#ff0000'
        )
    
    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Еда')
        self.assertEqual(self.category.type, 'expense')
    
    def test_operation_creation(self):
        operation = Operation.objects.create(
            user=self.user,
            category=self.category,
            amount=100.50,
            description='Покупка продуктов',
            date=timezone.now()
        )
        self.assertEqual(operation.amount, 100.50)
        self.assertEqual(operation.category, self.category)

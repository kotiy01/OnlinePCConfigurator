from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from components.models import CPU, Profile, SavedBuild
from prices.models import ShopItem
from decimal import Decimal


class APIIntegrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Тестовые данные
        self.cpu = CPU.objects.create(
            opendb_id="test-cpu-001",
            name="AMD Ryzen 7 7800X3D",
            brand="AMD",
            socket="AM5",
            cores_total=8,
            threads=16,
            base_clock=4.2,
            tdp=120,
            is_verified=True
        )
        
        # Магазинное предложение
        ct = ContentType.objects.get_for_model(CPU)
        self.shop_item = ShopItem.objects.create(
            content_type=ct,
            object_id=self.cpu.id,
            shop_name="regard.ru",
            name="AMD Ryzen 7 7800X3D OEM",
            price=Decimal("35000.00"),
            in_stock=True,
            url="https://regard.ru/product/123",
            extracted_mpn="100-000000910"
        )
        
        # Пользователь
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )


class CPUAPITests(APIIntegrationTestCase):
    def test_cpu_list_returns_verified_only(self):
        """API возвращает только верифицированные процессоры"""
        # Неверифицированный процессор
        CPU.objects.create(
            opendb_id="test-cpu-002",
            name="Unknown CPU",
            brand="Unknown",
            is_verified=False
        )
        
        response = self.client.get(reverse('cpu-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "AMD Ryzen 7 7800X3D")
    
    def test_cpu_list_filters_by_has_prices(self):
        """Фильтрация компонентов без цен"""
        # Создаём процессор без магазинных предложений
        cpu_no_price = CPU.objects.create(
            opendb_id="test-cpu-003",
            name="CPU Without Price",
            brand="AMD",
            socket="AM5",
            is_verified=True
        )
        
        response = self.client.get(reverse('cpu-list'), {'has_prices': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_cpu_retrieve_includes_min_price_and_shop_items(self):
        """Детальный ответ содержит минимальную цену и магазины"""
        response = self.client.get(reverse('cpu-detail', args=[self.cpu.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['min_price'], 35000.00)
        self.assertEqual(len(response.data['shop_items']), 1)
        self.assertEqual(response.data['shop_items'][0]['shop_name'], "regard.ru")


class AuthAPITests(APIIntegrationTestCase):
    def test_user_registration_creates_profile(self):
        """При регистрации автоматически создается профиль"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(user, 'profile'))
    
    def test_login_fails_with_wrong_password(self):
        """Неверный пароль возвращает ошибку"""
        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SavedBuildAPITests(APIIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)
    
    def test_create_saved_build(self):
        """Создание сохраненной сборки"""
        data = {
            'name': 'Моя первая сборка',
            'build_data': {
                'cpu': {'id': self.cpu.id, 'name': self.cpu.name, 'price': 35000},
                'totalPrice': 35000
            }
        }
        response = self.client.post(reverse('saved-builds'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SavedBuild.objects.count(), 1)
        self.assertEqual(SavedBuild.objects.first().user, self.user)
    
    def test_list_saved_builds_returns_only_user_builds(self):
        """Пользователь видит только свои сборки"""
        # Сборка для текущего пользователя
        SavedBuild.objects.create(
            user=self.user,
            name="Моя сборка",
            build_data={"cpu": {"name": "Ryzen 7"}}
        )
        # Другой пользователь
        other_user = User.objects.create_user(username="other", password="pass")
        SavedBuild.objects.create(
            user=other_user,
            name="Чужая сборка",
            build_data={"cpu": {"name": "Intel i9"}}
        )
        
        response = self.client.get(reverse('saved-builds'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Моя сборка")


class PublicBuildAPITests(APIIntegrationTestCase):
    def test_public_build_accessible_without_auth(self):
        """Публичный эндпоинт доступен без авторизации"""
        build = SavedBuild.objects.create(
            user=self.user,
            name="Публичная сборка",
            build_data={"cpu": {"name": "Ryzen 7", "price": 35000}}
        )
        self.client.force_authenticate(user=None)  # сбрасываем авторизацию
        
        response = self.client.get(reverse('public-build', args=[build.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Публичная сборка")
    
    def test_public_build_returns_404_for_nonexistent(self):
        """Несуществующая сборка возвращает 404"""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('public-build', args=[99999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
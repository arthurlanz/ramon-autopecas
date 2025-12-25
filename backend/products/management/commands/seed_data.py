from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula banco de dados com dados iniciais'
    
    def handle(self, *args, **options):
        self.stdout.write('Criando dados iniciais...')
        
        # Criar usuários
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@ramonautopecas.com',
                password='admin123',
                first_name='Ramon',
                last_name='Admin',
                role='owner'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuário admin criado'))
        
        if not User.objects.filter(username='anunciador').exists():
            advertiser = User.objects.create_user(
                username='anunciador',
                email='anunciador@ramonautopecas.com',
                password='anunciador123',
                first_name='João',
                last_name='Anunciador',
                role='advertiser'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuário anunciador criado'))
        
        # Criar categorias
        categories_data = [
            {'name': 'Motor', 'ml_category_id': 'MLB1743'},
            {'name': 'Suspensão', 'ml_category_id': 'MLB1744'},
            {'name': 'Freios', 'ml_category_id': 'MLB1745'},
            {'name': 'Elétrica', 'ml_category_id': 'MLB1746'},
            {'name': 'Carroceria', 'ml_category_id': 'MLB1747'},
            {'name': 'Filtros', 'ml_category_id': 'MLB1748'},
            {'name': 'Correias', 'ml_category_id': 'MLB1749'},
            {'name': 'Óleo e Fluidos', 'ml_category_id': 'MLB1750'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'ml_category_id': cat_data['ml_category_id'],
                    'description': f'Peças de {cat_data["name"].lower()}'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Categoria {cat_data["name"]} criada'))
        
        # Criar produtos de exemplo
        motor_cat = Category.objects.get(name='Motor')
        freios_cat = Category.objects.get(name='Freios')
        
        products_data = [
            {
                'title': 'Filtro de Óleo Mann W950/26',
                'category': motor_cat,
                'brand': 'Mann',
                'model': 'W950/26',
                'description': 'Filtro de óleo de alta qualidade para diversos veículos',
                'compatible_vehicles': 'VW Gol, Fox, Polo, Saveiro',
                'year_from': 2010,
                'year_to': 2024,
                'price': Decimal('45.90'),
                'cost_price': Decimal('28.50'),
                'stock_quantity': 50,
            },
            {
                'title': 'Pastilha de Freio Dianteira Cobreq',
                'category': freios_cat,
                'brand': 'Cobreq',
                'model': 'N-1234',
                'description': 'Pastilha de freio cerâmica de alta performance',
                'compatible_vehicles': 'VW Gol G5, G6, G7, Voyage',
                'year_from': 2008,
                'year_to': 2024,
                'price': Decimal('89.90'),
                'cost_price': Decimal('55.00'),
                'stock_quantity': 30,
            },
        ]
        
        owner = User.objects.filter(role='owner').first()
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                title=prod_data['title'],
                defaults={**prod_data, 'created_by': owner}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Produto {prod_data["title"]} criado'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Dados iniciais criados com sucesso!'))

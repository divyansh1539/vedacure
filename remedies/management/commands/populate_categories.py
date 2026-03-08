from django.core.management.base import BaseCommand
from remedies.models import Category


class Command(BaseCommand):
    help = 'Create 10 default categories for VedaCure'

    def handle(self, *args, **options):
        # Delete existing categories
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING('🗑️ Deleted existing categories'))

        categories = [
            {'name': 'Haircare Health', 'slug': 'haircare-health'},
            {'name': 'Skincare Health', 'slug': 'skincare-health'},
            {'name': 'Women\'s Health', 'slug': 'womens-health'},
            {'name': 'Immunity & Wellness', 'slug': 'immunity-wellness'},
            {'name': 'Cold, Cough & Fever', 'slug': 'cold-cough-fever'},
            {'name': 'ENT Health', 'slug': 'ent-health'},
            {'name': 'Digestive Health', 'slug': 'digestive-health'},
            {'name': 'Mental Wellness', 'slug': 'mental-wellness'},
            {'name': 'Pain Relief', 'slug': 'pain-relief'},
            {'name': 'Respiratory Health', 'slug': 'respiratory-health'},
        ]

        for cat_data in categories:
            category = Category.objects.create(
                name=cat_data['name'],
                slug=cat_data['slug']
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created category: {category.name}')
            )

        self.stdout.write(
            self.style.SUCCESS('\n✅ All 10 default categories created successfully!')
        )

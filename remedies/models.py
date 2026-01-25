from django.db import models

# Create your models here.

# Category like Skin, Hair, Digestive
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Problem like Acne, Hair Fall
class Problem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="problems")
    name = models.CharField(max_length=100)
    short_description = models.TextField()

    def __str__(self):
        return self.name


# Remedy details
class Remedy(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="remedies")
    remedy_name = models.CharField(max_length=200)
    ingredients = models.TextField()
    preparation_steps = models.TextField()
    how_to_use = models.TextField()
    frequency = models.CharField(max_length=100)
    precautions = models.TextField()
    why_it_works = models.TextField()
    disclaimer = models.TextField(default="This remedy is for educational purposes only.")

    def __str__(self):
        return self.remedy_name


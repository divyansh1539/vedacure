from django.db import models


# ================= CATEGORY =================
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ================= PROBLEM =================
class Problem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="problems"
    )

    name = models.CharField(max_length=100)

    about_problem = models.TextField()
    symptoms = models.TextField()

    short_description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ================= REMEDY =================
# ================= REMEDY =================
class Remedy(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="remedies"
    )

    remedy_name = models.CharField(max_length=200)

    ingredients = models.TextField()
    preparation_steps = models.TextField()
    how_to_use = models.TextField()
    frequency = models.TextField(blank=True)

    results_time = models.TextField(blank=True)
    why_it_works = models.TextField()

    precautions = models.TextField()
    who_should_not_use = models.TextField(blank=True)
    lifestyle_tips = models.TextField(blank=True)

    # ✅ ADD THIS PART (VERY IMPORTANT)
    class Meta:
        unique_together = ("problem", "remedy_name")

    def __str__(self):
        return f"{self.remedy_name} - {self.problem.name}"
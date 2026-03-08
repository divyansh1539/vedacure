from django.contrib import admin
from .models import Category, Problem, Remedy

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Remedy)
class RemedyAdmin(admin.ModelAdmin):
    list_display = ("id", "remedy_name", "problem")
    list_filter = ("problem",)
    search_fields = ("remedy_name",)
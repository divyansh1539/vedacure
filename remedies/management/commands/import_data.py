from django.core.management.base import BaseCommand
from django.conf import settings
from remedies.models import Category, Problem, Remedy

import json
import os


class Command(BaseCommand):
    help = "Import remedies data from JSON"

    def handle(self, *args, **kwargs):

        file_path = os.path.join(
            settings.BASE_DIR,
            "remedies",
            "data",
            "haircare.json"
        )

        # ✅ LOAD JSON
        with open(file_path, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        # ===============================
        # MAIN LOOP
        # ===============================
        for data in data_list:
            print("DEBUG DATA =>", data)

            # -------- CATEGORY --------
            category_obj, _ = Category.objects.get_or_create(
                name=data["category"]
            )

            # -------- PROBLEMS LOOP --------
            for problem_data in data["problems"]:

                # ✅ UPDATE OR CREATE (IMPORTANT FIX)
                problem_obj, _ = Problem.objects.update_or_create(
                    category=category_obj,
                    name=problem_data["name"],
                    defaults={
                        "short_description": problem_data.get("short_description", ""),
                        "about_problem": problem_data.get("about_problem", ""),
                        "symptoms": problem_data.get("symptoms", ""),
                    }
                )

                # -------- REMEDIES LOOP --------
                for remedy in problem_data["remedies"]:

                    # ✅ UPDATE OR CREATE (IMPORTANT FIX)
                    Remedy.objects.update_or_create(
                        problem=problem_obj,
                        remedy_name=remedy["remedy_name"],
                        defaults={
                            "ingredients": remedy.get("ingredients", ""),
                            "preparation_steps": remedy.get("preparation_steps", ""),
                            "how_to_use": remedy.get("how_to_use", ""),
                            "frequency": remedy.get("frequency", ""),
                            "results_time": remedy.get("results_time", ""),
                            "why_it_works": remedy.get("why_it_works", ""),
                            "precautions": remedy.get("precautions", ""),
                            "who_should_not_use": remedy.get("who_should_not_use", ""),
                            "lifestyle_tips": remedy.get("lifestyle_tips", ""),
                        }
                    )

        # ✅ SUCCESS MESSAGE
        self.stdout.write(
            self.style.SUCCESS("✅ Haircare data imported successfully!")
        )
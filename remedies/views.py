from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from openai import OpenAI
from django.conf import settings
from .models import Problem, Category

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# 🔥 DEFAULT REPLIES (PEHLE)
DEFAULT_REPLIES = {
    "hi": "Hi 👋 I am VedaBOT 🤖. How can I help you?",
    "hello": "Hello 😊 How can I assist you today?",
    "hyy": "Hey 👋 How can I help?",
    "how are you": "I am doing great 😄 Thanks for asking!",
    "who are you": "I am VedaBOT 🤖, your assistant for VedaCure.",
    "what is vedacure": "VedaCure is a platform for ancient Indian home remedies with AI support.",
    "bye": "Goodbye 👋 Stay healthy 🌿"
}
CATEGORY_DATA = {
    "haircare-health": {
        "title": "Haircare Health",
        "items": [
            "Hair Fall",
            "Dandruff",
            "Hair Growth",
            "Dry Hair",
            "Split Ends",
            "Hair Thinning",
            "Scalp Infection",
            "Grey Hair",
            "Baldness",
            "Excessive Hair Shedding",
        ],
    },

    "skincare-health": {
        "title": "Skincare Health",
        "items": [
            "Pimples",
            "blackheads",
            "Dry Skin",
            "Oily Skin",
            "Dull Skin",
            "Sun Tan",
            "Stretch Marks",
            "Scars",
            "Skin Redness", 
            "Rashes"
        ]
    },

    "womens-health": {
        "title": "Women's Health",
        "items": [
            "Irregular Periods",
            "Painful Period",
            "Menstrual Cramps",
            "Heavy Periods",
            "White Discharge",
            "Hormonal Imbalance Periods",
            "PCOS Symptoms",
            "Menopause Symptoms",
            "Back Pain During Periods",
            "Mood Swings",
        ]
    },

    "immunity-wellness": {
        "title": "Immunity & Wellness",
        "items": [
            "Weak Immunity",
            "Frequent Illness",
            "Low Energy",
            "Fatigue",
            "Weakness after Illness",
            "Tiredness",
            "Seasonal Allergies",
            "Poor Stamina"
        ]
    },

    "cold-cough-fever": {
        "title": "Cold, Cough & Fever",
        "items": [
            "Common Cold",
            "Cough",
            "Sore Throat",
            "Fever",
            "Nasal Congestion",
            "Sneezing",
            "Throat Pain",
            "Chest Congestion"
        ]
    },

    "ent-health": {
        "title": "ENT Health",
        "items": [
            "Eye Strain",
            "Dry Eyes",
            "Burning Eyes",
            "Red Eyes",
            "Ear Pain (Mild)",
            "Ear Blockage",
            "Nose Pain",
            "Nose Bleeding",
            "Throat Infection",
            "Tonsil irritation"
        ]
    },

    "digestive-health": {
        "title": "Digestive Health",
        "items": [
            "Acidity",
            "Constipation",
            "Bloating",
            "Indigestion",
            "Gas",
            "Diarrhea",
            "Stomach Pain",
            "Loss of Appetite"
        ]
    },

    "mental-wellness": {
        "title": "Mental Wellness",
        "items": [
            "Stress",
            "Anxiety",
            "Insomnia",
            "Depression",
            "Brain Fog",
            "Memory Loss",
            "Nervousness",
            "Worry"
        ]
    },

    "pain-relief": {
        "title": "Pain Relief",
        "items": [
            "Headache",
            "Migraine",
            "Back Pain",
            "Joint Pain",
            "Muscle Pain",
            "Neck Pain",
            "Body Aches",
            "Arthritis Pain"
        ]
    },

    "respiratory-health": {
        "title": "Respiratory Health",
        "items": [
            "Asthma",
            "Bronchitis",
            "Wheezing",
            "Shortness of Breath",
            "Chronic Cough",
            "Lung Congestion",
            "Breathing Difficulty",
            "Allergic Cough"
        ]
    },
}
def problem_detail(request, name):

    try:
        problem = Problem.objects.get(name__iexact=name)
        remedies = problem.remedies.all()

        return render(request, "problem_detail.html", {
            "problem": problem,
            "remedies": remedies,
        })

    except Problem.DoesNotExist:
        return render(request, "404.html")
    
def get_ai_response(user_message):
    if not user_message:
        return "Please ask something related to health or remedies."

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": """
You are VedaBOT, a natural Ayurvedic health assistant for VedaCure.

Rules:
- Answer like a human health expert.
- Explain WHY the problem happens.
- Suggest safe home remedies.
- Keep language simple and friendly.
- Do NOT mention AI or API.
- Give structured helpful answers.
"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_output_tokens=400,
        )

        return response.output_text

    except Exception as e:
        print("OpenAI Error:", e)
        return "⚠️ I'm having a small connection issue. Please try again."


# ================= HOME PAGE =================
def home(request):
    return render(request, 'home.html')

def remedies_page(request):
    categories = [
        {"slug": "haircare-health", "title": "Haircare Health"},
        {"slug": "skincare-health", "title": "Skincare Health"},
        {"slug": "womens-health", "title": "Women's Health"},
        {"slug": "immunity-wellness", "title": "Immunity & Wellness"},
        {"slug": "cold-cough-fever", "title": "Cold, Cough & Fever"},
        {"slug": "ent-health", "title": "ENT Health"},
        {"slug": "digestive-health", "title": "Digestive Health"},
        {"slug": "mental-wellness", "title": "Mental Wellness"},
        {"slug": "pain-relief", "title": "Pain Relief"},
        {"slug": "respiratory-health", "title": "Respiratory Health"},
    ]
    return render(request, "remedy_detail.html", {"categories": categories})

def ai_suggest(request):
    return render(request, "ai.html")

def about(request):
    return render(request, "about.html")

def blog(request):
    return render(request, "blog.html")

def contact(request):
    return render(request, "contact.html")

def category_detail(request, slug):
    try:
        # Get the Category object directly by slug
        category = Category.objects.get(slug=slug)
        
        # Filter problems using the ForeignKey relation
        problems = Problem.objects.filter(category=category).order_by('name')

        return render(request, "category.html", {
            "category_name": category.name,
            "problems": problems,
            "slug": slug
        })
    
    except Category.DoesNotExist:
        return render(request, "404.html")

def services(request):
    """
    Minimal services page view.

    Renders the clean Browse by Category layout defined in services.html.
    No dynamic data, images, or legacy remedy lists are passed here.
    """
    return render(request, "services.html")


# ================= VEDABOT API =================
@csrf_exempt
def vedabot_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    user_message = data.get("message", "").strip()

    # Default replies first
    for key in DEFAULT_REPLIES:
        if key in user_message.lower():
            return JsonResponse({"reply": DEFAULT_REPLIES[key]})

    # AI response
    ai_reply = get_ai_response(user_message)

    return JsonResponse({"reply": ai_reply})
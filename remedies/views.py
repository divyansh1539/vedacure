from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
import os
import random
import string
from google import genai
from django.conf import settings
from .models import Problem, Category
from django.utils import timezone
from datetime import timedelta

client = genai.Client(api_key=settings.GEMINI_API_KEY)

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
        return "Please ask something related to health."

    msg = user_message.lower()

    # ================= HAIR =================
    if "hair fall" in msg or "hair loss" in msg:
        return """Hair fall can happen due to stress, hormonal imbalance, or poor nutrition.

Natural remedies:
• Massage scalp with coconut oil + amla oil.
• Apply onion juice twice a week.
• Eat iron and protein rich foods like spinach and nuts."""

    if "dandruff" in msg:
        return """Dandruff is often caused by dry scalp or fungal growth.

Remedies:
• Apply neem oil or tea tree oil.
• Wash hair with mild herbal shampoo.
• Apply yogurt and lemon mask on scalp."""

    if "hair growth" in msg:
        return """For healthy hair growth:

• Massage scalp with castor oil.
• Eat protein rich foods.
• Use aloe vera gel on scalp."""

    # ================= SKIN =================
    if "pimples" in msg or "acne" in msg:
        return """Pimples are caused by excess oil and bacteria.

Natural remedies:
• Apply aloe vera gel.
• Use turmeric and honey mask.
• Drink plenty of water."""

    if "dry skin" in msg:
        return """For dry skin relief:

• Apply coconut oil or almond oil.
• Use aloe vera gel.
• Drink enough water daily."""

    if "oily skin" in msg:
        return """For oily skin:

• Wash face with mild cleanser.
• Apply multani mitti face pack.
• Avoid oily food."""

    # ================= DIGESTION =================
    if "gas" in msg or "bloating" in msg:
        return """Gas and bloating usually occur due to poor digestion.

Remedies:
• Drink warm water with lemon.
• Eat ginger or fennel seeds.
• Avoid heavy oily meals."""

    if "constipation" in msg:
        return """For constipation:

• Drink warm water in morning.
• Eat fiber rich foods like fruits.
• Consume soaked raisins or flax seeds."""

    if "stomach pain" in msg:
        return """Stomach pain may occur due to indigestion.

Natural remedies:
• Drink ginger tea.
• Take fennel seeds after meals.
• Avoid spicy food."""

    # ================= COLD / COUGH =================
    if "cold" in msg or "cough" in msg:
        return """For cold and cough relief:

• Drink ginger tea with honey.
• Take turmeric milk at night.
• Steam inhalation helps clear congestion."""

    if "sore throat" in msg:
        return """For sore throat:

• Gargle with warm salt water.
• Drink honey with ginger.
• Avoid cold drinks."""

    # ================= IMMUNITY =================
    if "immunity" in msg or "weakness" in msg:
        return """To boost immunity:

• Drink turmeric milk.
• Eat fruits and vegetables.
• Practice yoga and exercise regularly."""

    if "tired" in msg or "fatigue" in msg:
        return """Fatigue can occur due to lack of sleep or nutrition.

Remedies:
• Drink lemon honey water.
• Eat balanced diet.
• Take proper rest."""

    # ================= MENTAL =================
    if "stress" in msg or "anxiety" in msg:
        return """For stress relief:

• Practice meditation and yoga.
• Take deep breathing exercises.
• Drink herbal tea like tulsi."""

    if "sleep" in msg or "insomnia" in msg:
        return """For better sleep:

• Drink warm milk before bed.
• Avoid mobile screens before sleep.
• Maintain regular sleep schedule."""

    # ================= PAIN =================
    if "headache" in msg:
        return """For headache relief:

• Apply peppermint oil on temples.
• Drink ginger tea.
• Rest in a quiet dark room."""

    if "back pain" in msg:
        return """For back pain:

• Do light stretching exercises.
• Apply warm compress.
• Maintain good posture."""

    if "joint pain" in msg:
        return """For joint pain:

• Massage with warm sesame oil.
• Do light exercise.
• Eat anti-inflammatory foods like turmeric."""

    # ================= EYES / ENT =================
    if "eye strain" in msg or "dry eyes" in msg:
        return """For eye strain:

• Follow 20-20-20 rule.
• Blink frequently.
• Use cold water splash on eyes."""

    if "ear pain" in msg:
        return """For mild ear pain:

• Use warm compress.
• Avoid inserting objects in ear.
• Consult doctor if pain persists."""

    if "nose bleed" in msg:
        return """For nose bleeding:

• Sit upright and lean slightly forward.
• Apply cold compress on nose.
• Stay hydrated."""

    # ================= WOMEN HEALTH =================
    if "period" in msg or "menstrual" in msg:
        return """For menstrual discomfort:

• Drink warm ginger tea.
• Apply heating pad on abdomen.
• Practice light yoga."""

    if "pcos" in msg:
        return """PCOS management tips:

• Maintain healthy weight.
• Exercise regularly.
• Eat balanced diet."""

    # ================= DEFAULT =================
    return """Thank you for your question.

VedaBOT suggests natural Ayurvedic remedies and healthy lifestyle practices.

You can also explore remedies on VedaCure by selecting a health category."""

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
    if request.method == 'POST':
        # Get form data
        fullname = request.POST.get('fullname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip()
        company = request.POST.get('company', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validate required fields
        if not all([fullname, lastname, email, message]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact.html')
        
        # Prepare email content
        email_subject = 'New Enquiry from VedaCure Website'
        email_body = f"""
New Contact Form Submission from VedaCure Website

First Name: {fullname}
Last Name: {lastname}
Email Address: {email}
Company/Organization: {company if company else 'Not provided'}
Health Goals:
{message}

---
This is an automated message. Please reply to: {email}
        """
        
        try:
            # Send email to VedaCure
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['vedacureofficial@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, 'Your inquiry has been sent successfully! We will respond within 24 hours.')
        except Exception as e:
            print(f"Email sending error: {e}")
            messages.error(request, 'There was an error sending your inquiry. Please try again later.')
        
        return render(request, 'contact.html')
    
    return render(request, 'contact.html')

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

# ================= LOGIN & AUTHENTICATION =================
def login_page(request):
    """Render the login page and handle user login"""
    # If user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'login.html')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login user
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def signup_page(request):
    """Render the signup page and handle user registration"""
    # If user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        # Validate inputs
        if not all([full_name, username, email, password, confirm_password]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'signup.html')
        
        # Validate password match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')
        
        # Validate password length
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'signup.html')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken. Please choose another.')
            return render(request, 'signup.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return render(request, 'signup.html')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name
            )
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')


def logout_user(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
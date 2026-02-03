from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

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

# ================= HOME PAGE =================
def home(request):
    return render(request, 'home.html')

def remedies_page(request):
    return render(request, "remedy_detail.html")



# ================= VEDABOT API =================
@csrf_exempt
def vedabot_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    user_message = data.get("message", "").lower().strip()

    for key in DEFAULT_REPLIES:
        if key in user_message:
            return JsonResponse({"reply": DEFAULT_REPLIES[key]})

    return JsonResponse({
        "reply": "🤖 I am still learning. Please ask something related to health or remedies."
    })

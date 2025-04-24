# ai_coach/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings

from .models import CoachingSession
from .forms import CoachingForm
from openai import OpenAI


@login_required
def coach_home(request):
    if request.method == 'POST':
        form = CoachingForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            # pull category and question from the form
            category = form.cleaned_data.get('category', '')
            question = form.cleaned_data['question']
            session.response = get_ai_coaching_response(question, category)
            session.save()
            messages.success(request, "Your coaching advice is ready!")
            return redirect('ai_coach:home')
    else:
        form = CoachingForm()

    recent_sessions = CoachingSession.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    return render(request, 'ai_coach/home.html', {
        'form': form,
        'recent_sessions': recent_sessions,
        'categories': CoachingSession.CATEGORY_CHOICES,
    })


@login_required
def coaching_history(request):
    category = request.GET.get('category', '')
    sessions = CoachingSession.objects.filter(user=request.user)

    # filter by category if provided
    if category and category in dict(CoachingSession.CATEGORY_CHOICES):
        sessions = sessions.filter(category=category)

    # filter by favorites only if requested
    favorites_only = request.GET.get('favorites') == 'true'
    if favorites_only:
        sessions = sessions.filter(is_favorite=True)

    return render(request, 'ai_coach/history.html', {
        'sessions': sessions,
        'current_category': category,
        'favorites_only': favorites_only,
        'categories': CoachingSession.CATEGORY_CHOICES,
    })


@login_required
def toggle_favorite(request, session_id):
    session = get_object_or_404(
        CoachingSession,
        id=session_id,
        user=request.user
    )
    session.is_favorite = not session.is_favorite
    session.save()
    return JsonResponse({
        'status': 'success',
        'is_favorite': session.is_favorite
    })


def get_ai_coaching_response(question: str, category: str) -> str:
    """
    Sends the question (with optional category tag) to OpenAI and returns the coach response.
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    system_prompt = (
        "You are an expert fitness coach."
        "Keep your responses **very brief** (no more than **3 sentences** or **4 bullet points**)."  
        "Use clear, simple language so beginners can understand."  
        "Focus only on the core advice—no extra fluff."
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"[{category}] {question}".strip()}
            ],
            max_tokens=300,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return "Sorry, we're having trouble connecting to the coaching service right now."

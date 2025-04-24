# ai_coach/views.py

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.conf import settings
from django.urls import reverse

from .models import CoachingSession
from .forms import CoachingForm
from openai import OpenAI
import markdown as md  # for rendering **bold**, lists, etc.

@login_required
def coach_home(request):
    if request.method == 'POST':
        form = CoachingForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.response = get_ai_coaching_response(
                request.user,
                form.cleaned_data['question'],
                form.cleaned_data['category']
            )
            session.save()
            messages.success(request, "Your coaching advice is ready!")
            # Redirect with anchor to the new session
            url = reverse('ai_coach:home') + f"#session-{session.id}"
            return redirect(url)
    else:
        form = CoachingForm()

    recent_sessions = (
        CoachingSession.objects
        .filter(user=request.user)
        .order_by('-created_at')[:5]
    )
    return render(request, 'ai_coach/home.html', {
        'form': form,
        'recent_sessions': recent_sessions,
        'categories': CoachingSession.CATEGORY_CHOICES,
    })

@login_required
def coaching_history(request):
    category = request.GET.get('category', '')
    qs = CoachingSession.objects.filter(user=request.user)
    if category in dict(CoachingSession.CATEGORY_CHOICES):
        qs = qs.filter(category=category)
    if request.GET.get('favorites') == 'true':
        qs = qs.filter(is_favorite=True)
    return render(request, 'ai_coach/history.html', {
        'sessions': qs,
        'current_category': category,
        'favorites_only': request.GET.get('favorites') == 'true',
        'categories': CoachingSession.CATEGORY_CHOICES,
    })

@login_required
@require_POST
def toggle_favorite(request, session_id):
    session = get_object_or_404(CoachingSession, id=session_id, user=request.user)
    session.is_favorite = not session.is_favorite
    session.save()
    return JsonResponse({'status': 'success', 'is_favorite': session.is_favorite})

@login_required
@require_POST
def toggle_helpful(request, session_id):
    try:
        payload = json.loads(request.body)
        helpful_flag = payload.get('helpful')
    except json.JSONDecodeError:
        return HttpResponseBadRequest()

    session = get_object_or_404(CoachingSession, id=session_id, user=request.user)
    session.is_helpful = (helpful_flag == 'yes')
    session.save()
    return JsonResponse({'status': 'success', 'is_helpful': session.is_helpful})

def get_ai_coaching_response(user, question, category):
    # Pull last 3 sessions for context
    history = CoachingSession.objects.filter(user=user).order_by('-created_at')[:3]
    messages = [
        {"role": "system", "content": (
            "You are an expert fitness coach. Keep your responses very brief "
            "(no more than 3 sentences or 4 bullet points). Use clear, simple "
            "language so beginners can understand. Focus only on the core advice—no extra fluff."
        )}
    ]
    for s in history:
        messages.append({"role": "user",      "content": f"[{s.category}] {s.question}"})
        messages.append({"role": "assistant", "content": s.response})

    messages.append({"role": "user", "content": f"[{category}] {question}"})

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
        temperature=0.4,
        top_p=0.9,
    )

    raw_md = resp.choices[0].message.content.strip()
    # Convert Markdown to HTML so **bold**, lists, etc. render properly
    return md.markdown(raw_md, extensions=['extra', 'sane_lists'])

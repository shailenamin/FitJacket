from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CoachingSession
from .forms import CoachingForm
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

@login_required
def coach_home(request):
    form = CoachingForm()
    recent_sessions = CoachingSession.objects.filter(user=request.user).order_by('-created_at')[:3]
    
    return render(request, 'ai_coach/home.html', {
        'form': form,
        'recent_sessions': recent_sessions,
    })

@login_required
def ask_coach(request):
    if request.method == 'POST':
        form = CoachingForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            
            # Generate AI response
            response = get_ai_coaching_response(question)
            
            # Save the question and response
            session = form.save(commit=False)
            session.user = request.user
            session.response = response
            session.save()
            
            messages.success(request, "Your coaching advice is ready!")
            return redirect('ai_coach:home')
    else:
        form = CoachingForm()
    
    return render(request, 'ai_coach/ask.html', {'form': form})

@login_required
def coaching_history(request):
    sessions = CoachingSession.objects.filter(user=request.user)
    return render(request, 'ai_coach/history.html', {'sessions': sessions})

def get_ai_coaching_response(question):
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        system_prompt = """
        You are an expert fitness coach who provides helpful, encouraging, and personalized fitness advice.
        Focus on being supportive while giving scientifically sound information about exercise, nutrition, 
        and healthy habits. Keep responses concise and beginner-friendly. Structure your advice with bullet points where appropriate.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
        )
        
        coaching_advice = response.choices[0].message.content.strip()
        return coaching_advice
        
    except Exception as e:
        print(f"Error with AI request: {e}")
        return "Sorry, we're having trouble connecting to the coaching service right now. Please try again later."

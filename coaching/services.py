import openai
from django.conf import settings

class AICoachService:
    @staticmethod
    def get_coaching_response(user_query, user_profile=None, workout_history=None):
        try:
            openai.api_key = settings.OPENAI_API_KEY
            
            context = "You are FitJacket's AI fitness coach. Provide helpful fitness advice."
            
            if user_profile:
                context += f"\nUser Profile: Age: {user_profile.age}, Goals: {user_profile.goals}, "
                context += f"Fitness Level: {user_profile.fitness_level}"
                
            if workout_history:
                context += "\nRecent workouts:"
                for workout in workout_history[:3]:
                    context += f"\n- {workout.date}: {workout.activity_type}, Duration: {workout.duration} min"
            
            messages = [
                {"role": "system", "content": context},
                {"role": "user", "content": user_query}
            ]
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=500,
                # temperature=0.7
            )
            
            return response.choices[0].message['content']
            
        except Exception as e:
            print(f"Error getting AI coaching response: {e}")
            return "I'm sorry, I'm having trouble providing coaching advice right now. Please try again later."

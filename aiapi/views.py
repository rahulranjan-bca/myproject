from django.shortcuts import render,redirect
from .services import ApiServices
from django.urls import reverse
gemini_service = ApiServices()
def text_generator(request):
    context = {}
    prompt=""
    ai_response=""
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        if prompt:
            ai_response = gemini_service.textQuery(prompt)
    context = {"prompt": prompt, "response":ai_response}
    return render(request, "text_gen.html",context)

# Create your views here.
def generate_quiz(request):
    context = {}

    if request.method == "POST":
        topic = request.POST.get("topic")
        num_questions = request.POST.get("num_questions")
        difficulty = request.POST.get("difficulty")

        if topic and num_questions and difficulty:
            try:
                num_questions = int(num_questions)
                difficulty = int(difficulty)
                
                # Call the Gemini service
                
                quiz_data = gemini_service.generate_quiz(topic, num_questions, difficulty)

                if quiz_data:
                    request.session['quiz_data'] = quiz_data['questions']  # list of Question objects
                    request.session['topic'] = topic
                    return redirect(reverse('take_quiz'))
                else:
                    context['error'] = "Quiz data format is invalid."

            except ValueError:
                context['error'] = "Invalid numbers provided for questions or difficulty."
            except Exception as e:
                context['error'] = f"Failed to generate the quiz. Please try again. {e}"

    return render(request, "quiz_generator.html", context)


def take_quiz(request):
    """Step 2: Displays the questions along with a matching countdown timer."""
    questions = request.session.get('quiz_data')
    topic = request.session.get('topic')
    
    # Guard clause: Redirect if user tries to access the quiz directly without generating it
    if not questions:
        return redirect(reverse('generate_quiz'))
        
    # Enforce time limits: 1 minute (60 seconds) * total number of questions
    total_time_seconds = len(questions) * 60

    context = {
        "questions": questions,
        "topic": topic,
        "total_time": total_time_seconds
    }
    return render(request, "quiz_play.html", context)

def quiz_results(request):
    """Step 3: Compares submitted answers against session data and tallies scores."""
    if request.method != "POST":
        return redirect(reverse('generate_quiz'))

    questions = request.session.get('quiz_questions', [])
    topic = request.session.get('quiz_topic', '')

    if not questions:
        return redirect(reverse('generate_quiz'))

    score = 0
    detailed_results = []

    # Loop through retrieved session questions to evaluate user form responses
    for i, q in enumerate(questions):
        user_answer = request.POST.get(f"question_{i}")
        is_correct = (user_answer == q['correct_answer'])
        
        if is_correct:
            score += 1

        detailed_results.append({
            "question_text": q['question_text'],
            "options": q['options'],
            "correct_answer": q['correct_answer'],
            "user_answer": user_answer if user_answer else "Skipped / Timed Out",
            "is_correct": is_correct,
            "explanation": q['explanation']
        })

    context = {
        "topic": topic,
        "score": score,
        "total_questions": len(questions),
        "percentage": int((score / len(questions)) * 100) if questions else 0,
        "results": detailed_results
    }
    
    return render(request, "quiz_results.html", context)
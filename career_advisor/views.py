from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import os
import sys

# Import our RAG service
from .rag_service import rag_service

# Add src to path for our existing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.pdf_parser import extract_text_from_pdf
from utils.resume_parser import parse_resume

def home(request):
    """Home page view"""
    return render(request, 'career_advisor/home.html')

def upload_resume(request):
    """Handle resume upload"""
    if request.method == 'POST':
        print(f"DEBUG: POST request received")
        print(f"DEBUG: Files in request: {list(request.FILES.keys())}")
        
        if 'resume' in request.FILES:
            resume_file = request.FILES['resume']
            print(f"DEBUG: Resume file found: {resume_file.name}")
            
            # Save file temporarily
            file_path = os.path.join('media', 'resumes', resume_file.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb+') as destination:
                for chunk in resume_file.chunks():
                    destination.write(chunk)
            
            print(f"DEBUG: File saved to: {file_path}")
            
            # Initialize RAG pipeline
            if rag_service.initialize_rag(file_path):
                print(f"DEBUG: RAG pipeline initialized successfully")
                messages.success(request, 'Resume uploaded and AI analysis initialized successfully!')
                return redirect('career_advisor:analyze_resume')
            else:
                print(f"DEBUG: RAG pipeline failed, trying fallback")
                # Fallback to basic parsing if RAG fails
                try:
                    import sys
                    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
                    from utils.pdf_parser import extract_text_from_pdf
                    from utils.resume_parser import parse_resume
                    
                    raw_text = extract_text_from_pdf(file_path)
                    parsed_data = parse_resume(raw_text)
                    
                    # Store in session for analysis
                    request.session['resume_data'] = parsed_data
                    request.session['resume_file'] = file_path
                    
                    print(f"DEBUG: Fallback parsing successful")
                    messages.warning(request, 'Resume uploaded with basic analysis. AI features may be limited.')
                    return redirect('career_advisor:analyze_resume')
                    
                except Exception as e:
                    print(f"DEBUG: Error in fallback parsing: {e}")
                    messages.error(request, f'Error processing resume: {str(e)}')
                    return redirect('career_advisor:home')
        else:
            print(f"DEBUG: No resume file in request")
            messages.error(request, 'No resume file uploaded.')
            return redirect('career_advisor:upload_resume')
    
    print(f"DEBUG: GET request, rendering upload form")
    return render(request, 'career_advisor/upload.html')

def analyze_resume(request):
    """Show resume analysis"""
    # Try to get data from RAG service first
    resume_data = rag_service.get_resume_data()
    
    if not resume_data:
        # Fallback to session data
        resume_data = request.session.get('resume_data')
        if not resume_data:
            messages.warning(request, 'Please upload a resume first.')
            return redirect('career_advisor:home')
    
    # Get cache info for performance monitoring
    cache_info = rag_service.get_cache_info()
    
    context = {
        'resume_data': resume_data,
        'skills_count': len(resume_data.get('skills', [])),
        'projects_count': len(resume_data.get('projects', [])),
        'education_count': len(resume_data.get('education', [])),
        'experience_count': len(resume_data.get('experience', [])),
        'rag_available': rag_service.is_available(),
        'cache_info': cache_info,
    }
    
    return render(request, 'career_advisor/analyze.html', context)

def skills_gap_analysis(request):
    """Skills gap analysis view"""
    resume_data = rag_service.get_resume_data() or request.session.get('resume_data')
    if not resume_data:
        messages.warning(request, 'Please upload a resume first.')
        return redirect('career_advisor:home')
    
    if request.method == 'POST':
        target_role = request.POST.get('target_role', 'Data Scientist')
        
        # Try RAG-based analysis first
        if rag_service.is_available():
            analysis = rag_service.analyze_skills_gap_rag(target_role)
            if 'error' not in analysis:
                # RAG analysis successful
                context = {
                    'resume_data': resume_data,
                    'analysis': analysis,
                    'target_role': target_role,
                    'rag_used': True,
                }
                return render(request, 'career_advisor/skills_gap.html', context)
        
        # Fallback to rule-based analysis
        analysis = analyze_skills_gap_fallback(resume_data, target_role)
        
        context = {
            'resume_data': resume_data,
            'analysis': analysis,
            'target_role': target_role,
            'rag_used': False,
        }
        
        return render(request, 'career_advisor/skills_gap.html', context)
    
    return render(request, 'career_advisor/skills_gap_form.html', {'resume_data': resume_data})

def career_paths(request):
    """Career path suggestions view"""
    resume_data = rag_service.get_resume_data() or request.session.get('resume_data')
    if not resume_data:
        messages.warning(request, 'Please upload a resume first.')
        return redirect('career_advisor:home')
    
    # Get career path suggestions
    career_paths = suggest_career_paths(resume_data)
    
    context = {
        'resume_data': resume_data,
        'career_paths': career_paths,
        'rag_available': rag_service.is_available(),
    }
    
    return render(request, 'career_advisor/career_paths.html', context)

def career_chat(request):
    """Career advice chat view"""
    resume_data = rag_service.get_resume_data() or request.session.get('resume_data')
    if not resume_data:
        messages.warning(request, 'Please upload a resume first.')
        return redirect('career_advisor:home')
    
    if request.method == 'POST':
        question = request.POST.get('question', '')
        if question:
            # Try RAG-based response first
            if rag_service.is_available():
                rag_response = rag_service.get_career_advice(question)
                if 'error' not in rag_response:
                    answer = rag_response.get('answer', 'I apologize, but I couldn\'t generate a response.')
                    return JsonResponse({'answer': answer, 'rag_used': True})
            
            # Fallback to rule-based response
            answer = get_career_advice_fallback(question, resume_data)
            return JsonResponse({'answer': answer, 'rag_used': False})
    
    context = {
        'resume_data': resume_data,
        'rag_available': rag_service.is_available(),
    }
    return render(request, 'career_advisor/chat.html', context)

def learning_roadmap(request):
    """Learning roadmap view"""
    resume_data = rag_service.get_resume_data() or request.session.get('resume_data')
    if not resume_data:
        messages.warning(request, 'Please upload a resume first.')
        return redirect('career_advisor:home')
    
    # Generate learning roadmap
    roadmap = generate_learning_roadmap(resume_data)
    
    context = {
        'resume_data': resume_data,
        'roadmap': roadmap,
        'rag_available': rag_service.is_available(),
    }
    
    return render(request, 'career_advisor/roadmap.html', context)

def performance_status(request):
    """Show RAG performance and caching status"""
    cache_info = rag_service.get_cache_info()
    
    context = {
        'cache_info': cache_info,
        'rag_available': rag_service.is_available(),
    }
    
    return render(request, 'career_advisor/performance.html', context)

# Fallback functions (when RAG is not available)
def analyze_skills_gap_fallback(resume_data, target_role):
    """Analyze skills gap for a specific role (fallback)"""
    role_skills = {
        "data scientist": ["Python", "SQL", "Machine Learning", "Statistics", "Data Visualization"],
        "software engineer": ["Programming", "Data Structures", "Algorithms", "System Design", "Testing"],
        "product manager": ["Product Strategy", "User Research", "Data Analysis", "Leadership", "Agile"],
        "data analyst": ["SQL", "Excel", "Python", "Data Visualization", "Statistical Analysis"],
        "ml engineer": ["Python", "Machine Learning", "Deep Learning", "MLOps", "Data Engineering"]
    }
    
    target_skills = role_skills.get(target_role.lower(), [])
    current_skills = set(resume_data.get("skills", []))
    
    # Find missing skills
    missing_skills = [skill for skill in target_skills if skill.lower() not in current_skills]
    
    return {
        "target_role": target_role,
        "current_skills": list(current_skills),
        "missing_skills": missing_skills,
        "recommendations": generate_skill_recommendations(missing_skills)
    }

def generate_skill_recommendations(missing_skills):
    """Generate specific recommendations for missing skills"""
    recommendations = []
    for skill in missing_skills:
        if "python" in skill.lower():
            recommendations.append(f"Learn {skill}: Start with Codecademy or freeCodeCamp Python courses")
        elif "sql" in skill.lower():
            recommendations.append(f"Learn {skill}: Practice on LeetCode or HackerRank SQL challenges")
        elif "machine learning" in skill.lower():
            recommendations.append(f"Learn {skill}: Take Andrew Ng's ML course on Coursera")
        elif "statistics" in skill.lower():
            recommendations.append(f"Learn {skill}: Take Statistics courses on Khan Academy or edX")
        elif "data visualization" in skill.lower():
            recommendations.append(f"Learn {skill}: Master Tableau, Power BI, or Python libraries like Matplotlib")
        else:
            recommendations.append(f"Develop {skill}: Research online courses and practice projects")
    
    return recommendations

def suggest_career_paths(resume_data):
    """Suggest potential career paths based on current skills"""
    skills = set(resume_data.get("skills", []))
    
    career_paths = []
    if any("python" in skill.lower() for skill in skills):
        career_paths.append("Data Scientist")
        career_paths.append("Software Engineer")
    if any("sql" in skill.lower() for skill in skills):
        career_paths.append("Data Analyst")
        career_paths.append("Business Intelligence Developer")
    if any("machine learning" in skill.lower() for skill in skills):
        career_paths.append("ML Engineer")
        career_paths.append("AI Researcher")
    if any("java" in skill.lower() for skill in skills):
        career_paths.append("Java Developer")
        career_paths.append("Android Developer")
        
    return career_paths or ["General Software Developer", "IT Consultant"]

def get_career_advice_fallback(question, resume_data):
    """Provide career advice based on the question (fallback)"""
    question_lower = question.lower()
    
    if "skill" in question_lower and "gap" in question_lower:
        return "I can help you analyze skills gaps! Use the Skills Gap Analysis feature to see what skills you need for your target role."
    
    elif "career" in question_lower and "path" in question_lower:
        return "Great question! Use Career Path Suggestions to see what career paths align with your current skills and background."
    
    elif "resume" in question_lower:
        skills_count = len(resume_data.get('skills', []))
        projects_count = len(resume_data.get('projects', []))
        return f"Your resume shows {skills_count} skills and {projects_count} projects. You're well-positioned for tech roles!"
    
    elif "python" in question_lower:
        if any("python" in skill.lower() for skill in resume_data.get("skills", [])):
            return "Great! You already have Python skills. Consider building more projects and learning advanced topics like Django, Flask, or data science libraries."
        else:
            return "Python is a great skill to add! Start with basic syntax, then move to web development or data science depending on your interests."
    
    else:
        return "I'm here to help with your career! You can ask me about skills, career paths, resume improvement, or use the interactive features above."

def generate_learning_roadmap(resume_data):
    """Generate learning roadmap based on skills"""
    skills = set(resume_data.get("skills", []))
    
    roadmap = {
        "python_path": [],
        "java_path": [],
        "data_path": [],
        "general": []
    }
    
    if any("python" in skill.lower() for skill in skills):
        roadmap["python_path"] = [
            "Advanced Python (Decorators, Generators)",
            "Web Development (Django/Flask)",
            "Data Science Libraries (Pandas, NumPy)",
            "Machine Learning (Scikit-learn)"
        ]
    
    if any("java" in skill.lower() for skill in skills):
        roadmap["java_path"] = [
            "Advanced Java (Collections, Streams)",
            "Spring Framework",
            "Microservices Architecture",
            "Cloud Deployment (AWS/Azure)"
        ]
    
    if any("sql" in skill.lower() for skill in skills):
        roadmap["data_path"] = [
            "Advanced SQL (Window Functions)",
            "Data Visualization (Tableau, Power BI)",
            "Business Intelligence",
            "Data Engineering"
        ]
    
    roadmap["general"] = [
        "Build portfolio projects",
        "Contribute to open source",
        "Network and attend tech meetups",
        "Stay updated with industry trends"
    ]
    
    return roadmap

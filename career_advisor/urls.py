from django.urls import path
from . import views

app_name = 'career_advisor'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('analyze/', views.analyze_resume, name='analyze_resume'),
    path('skills-gap/', views.skills_gap_analysis, name='skills_gap_analysis'),
    path('career-paths/', views.career_paths, name='career_paths'),
    path('chat/', views.career_chat, name='career_chat'),
    path('roadmap/', views.learning_roadmap, name='learning_roadmap'),
    path('performance/', views.performance_status, name='performance_status'),
] 
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),   
    path('register/', views.register, name='register'),
    path('', views.home_view, name='home'),
    path('study-sessions/', views.study_sessions_view, name='study_sessions'),
    path('resources/', views.resources_view, name='resources'),
    path('about/', views.about_view, name='about'),
    path('flashcards/', views.flashcards_view, name='flashcards'),
    path('flashcards/create-deck/', views.create_deck_view, name='create_deck'),
    path('flashcards/deck/<int:deck_id>/', views.deck_detail_view, name='deck_detail'),
    path('deck/<int:deck_id>/study/', views.study_flashcards_view, name='study_flashcards'),
    
    path('timer/', views.timer_page, name='timer'),
    path('reviews/', views.review_page, name='review_page'),
    path('study-groups/', views.study_groups_view, name='study_groups'),
    path('study-groups/create/', views.create_study_group, name='create_study_group'),
    path('study-groups/<int:group_id>/', views.study_group_detail, name='study_group_detail'),
    path('study-groups/<int:group_id>/join/', views.join_study_group, name='join_study_group'),
    path('study-groups/<int:group_id>/leave/', views.leave_study_group, name='leave_study_group'),
    
]
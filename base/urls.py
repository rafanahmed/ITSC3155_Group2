from django.urls import path
from . import views

urlpatterns = [
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
]
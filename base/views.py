from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import FlashcardDeck, Flashcard, Review
from .forms import FlashcardDeckForm, FlashcardForm, ReviewForm, RegisterForm

def login_view(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Use Django's built-in AuthenticationForm
        if form.is_valid():
            user = form.get_user()  # Get the authenticated user
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, 'Invalid username or password.')  # Show error message if form is invalid
    else:
        form = AuthenticationForm()  # Initialize an empty form for GET requests

    return render(request, 'base/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'base/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')

def home_view(request):
    return render(request, 'base/base.html')

def study_sessions_view(request):
    return render(request, 'base/study_sessions.html')

def resources_view(request):
    return render(request, 'base/resources.html')

def about_view(request):
    return render(request, 'base/about.html')

@login_required
def flashcards_view(request):
    decks = FlashcardDeck.objects.all()
    return render(request, 'base/flashcards.html', {'decks': decks})

@login_required
def create_deck_view(request):
    if request.method == 'POST':
        form = FlashcardDeckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flashcards')  # Changed from 'deck_list' to 'flashcards'
    else:
        form = FlashcardDeckForm()
    return render(request, 'base/create_deck.html', {'form': form})

@login_required
def deck_detail_view(request, deck_id):
    deck = get_object_or_404(FlashcardDeck, id=deck_id)
    cards = deck.flashcards.all()

    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.deck = deck
            flashcard.save()
            return redirect('deck_detail', deck_id=deck.id)
    else:
        form = FlashcardForm()

    return render(request, 'base/deck_detail.html', {'deck': deck, 'cards': cards, 'form': form})

@login_required
def study_flashcards_view(request, deck_id):
    deck = get_object_or_404(FlashcardDeck, id=deck_id)
    cards = deck.flashcards.all()
    current_card_index = int(request.GET.get('card', 0))

    # Handle empty deck case
    if not cards.exists():
        messages.warning(request, "This deck is empty. Add flashcards to study.")
        return redirect('deck_detail', deck_id=deck.id)

    # Ensure current_card_index is within bounds
    if current_card_index >= len(cards):
        current_card_index = 0
        current_card = cards[0]
    else:
        current_card = cards[current_card_index]

    next_card_index = (current_card_index + 1) % len(cards)
    prev_card_index = (current_card_index - 1) % len(cards)

    return render(request, 'base/study_flashcards.html', {
        'deck': deck,
        'current_card': current_card,
        'next_card_index': next_card_index,
        'prev_card_index': prev_card_index,
        'current_card_index': current_card_index,
        'total_cards': len(cards),
    })

@login_required
def delete_flashcard_view(request, deck_id, card_id):
    deck = get_object_or_404(FlashcardDeck, id=deck_id)
    flashcard = get_object_or_404(Flashcard, id=card_id, deck=deck)
    
    if request.method == 'POST':
        flashcard.delete()
        messages.success(request, 'Flashcard deleted successfully!')
        return redirect('deck_detail', deck_id=deck.id)
    
    return redirect('deck_detail', deck_id=deck.id)

def timer_page(request):
    return render(request, 'base/timer.html')

@login_required
def delete_deck_view(request, deck_id):
    deck = get_object_or_404(FlashcardDeck, id=deck_id)
    
    if request.method == 'POST':
        deck.delete()
        messages.success(request, 'Deck deleted successfully!')
        return redirect('flashcards')
    
    return redirect('flashcards')

@login_required
def review_page(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Associate the current user
            review.save()
            return redirect('review_page')
    
    sort_by = request.GET.get('sort', 'date')
    
    if sort_by == 'rating':
        reviews = Review.objects.all().order_by('-stars', '-created_at')
    else:
        reviews = Review.objects.all().order_by('-created_at')
    
    form = ReviewForm()
    return render(request, 'base/reviews.html', {
        'form': form,
        'reviews': reviews
    })
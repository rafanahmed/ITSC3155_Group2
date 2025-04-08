from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import FlashcardDeck, Flashcard, Review
from .forms import FlashcardDeckForm, FlashcardForm, ReviewForm, RegisterForm
from .models import StudyGroup
from .forms import StudyGroupForm
from .forms import GroupMessageForm
from django.http import JsonResponse


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
            return redirect('deck_list')
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

    if current_card_index < len(cards):
        current_card = cards[current_card_index]
    else:
        current_card = cards[0]
        current_card_index = 0

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

def timer_page(request):
    return render(request, 'base/timer.html')

@login_required
def review_page(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_page')
    else:
        form = ReviewForm()

    reviews = Review.objects.all()
    return render(request, 'base/reviews.html', {'form': form, 'reviews': reviews})

@login_required
def study_groups_view(request):
    user_groups = request.user.study_groups.all()
    all_groups = StudyGroup.objects.all()
    
    return render(request, 'base/study_groups.html', {
        'user_groups': user_groups,
        'all_groups': all_groups
    })

@login_required
def create_study_group(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            # Add the creator as a member
            group.members.add(request.user)
            messages.success(request, f"Study group '{group.name}' created successfully!")
            return redirect('study_group_detail', group_id=group.id)
    else:
        form = StudyGroupForm()
    
    return render(request, 'base/create_study_group.html', {'form': form})

@login_required
def study_group_detail(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    messages_list = group.messages.all().order_by('created_at')
    
    if request.method == 'POST':
        message_form = GroupMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.group = group
            message.sender = request.user
            message.save()
            
            # Return JSON response for WebSocket fallback
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': message.content,
                    'username': request.user.username,
                    'timestamp': message.created_at.isoformat(),
                    'is_current_user': True
                })
            return redirect('study_group_detail', group_id=group.id)
    
    return render(request, 'base/study_group_detail.html', {
        'group': group,
        'messages_list': messages_list,
        'message_form': GroupMessageForm()
    })

@login_required
def join_study_group(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    
    if request.user not in group.members.all():
        group.members.add(request.user)
        messages.success(request, f"You've joined '{group.name}'!")
    else:
        messages.info(request, f"You're already a member of '{group.name}'")
    
    return redirect('study_group_detail', group_id=group.id)

@login_required
def leave_study_group(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    
    if request.user in group.members.all():
        group.members.remove(request.user)
        messages.info(request, f"You've left '{group.name}'")
    
    return redirect('study_groups')

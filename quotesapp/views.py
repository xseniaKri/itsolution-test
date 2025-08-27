from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Count, Q
from .models import Quote, Vote, Source
from django.http import JsonResponse
import random
from django.contrib.auth import login
from .forms import CustomUserCreationForm, QuoteForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.source = form.cleaned_data['source_instance']
            quote.creator = request.user
            quote.save()
            return redirect('index')
    else:
        form = QuoteForm()
    return render(request, "add_quote.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    quotes_list = list(user.quotes.all())
    return render(request, "registration/profile.html", {"user": user, "quotes_list": quotes_list})

@login_required
def vote(request, quote_id, value):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        quote = get_object_or_404(Quote, id=int(quote_id))
        value = int(value)

        vote_obj, created = Vote.objects.get_or_create(
            quote=quote,
            user=request.user,
            defaults={'value': value}
        )

        if not created:
            vote_obj.value = value
            vote_obj.save()

        data = {
            'likes': quote.likes_count(),
            'dislikes': quote.dislikes_count()
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def index(request):
    quotes = list(Quote.objects.all())

    weights = [q.weight for q in quotes]

    quote = random.choices(quotes, weights=weights, k=1)[0]

    quote.views += 1
    quote.save(update_fields=["views"])

    views = quote.views
    text = quote.text
    likes = quote.likes_count()
    dislikes = quote.dislikes_count()
    source = quote.source.category + " " + quote.source.name
    creator = quote.creator.username

    return render(
        request,
        'index.html',
        context={'quote': quote, 'views': views, 'text': text, 'likes': likes, 'dislikes': dislikes, 'source': source, 'creator': creator},
    )

class PopularListView(generic.ListView):
    model = Quote
    context_object_name = 'top_5_quotes'
    template_name = 'most_popular.html'

    def get_queryset(self):
        return Quote.objects.annotate(
            likes_total=Count('votes', filter=Q(votes__value=1))
        ).order_by('-likes_total')[:5]
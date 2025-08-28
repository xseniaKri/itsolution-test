import random

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .forms import CustomUserCreationForm, QuoteForm
from .models import Favourites, Quote, Vote


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
def add_favourite(request, quote_id):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        quote = get_object_or_404(Quote, id=int(quote_id))

        favourite, created = Favourites.objects.get_or_create(
            quote=quote,
            owner=request.user,
        )

        if not created:
            favourite.delete()
            return JsonResponse({"favourite": False})

        return JsonResponse({"favourite": True})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.source = form.cleaned_data["source_instance"]
            quote.creator = request.user
            quote.save()
            return redirect("index")
    else:
        form = QuoteForm()
    return render(request, "add_quote.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    quotes_list = list(user.quotes.all())
    favs = list(user.favourites.all())
    fav_quotes = [el.quote for el in favs]
    return render(
        request,
        "registration/profile.html",
        {"user": user, "quotes_list": quotes_list, "fav_quotes": fav_quotes},
    )


@login_required
def vote(request, quote_id, value):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        quote = get_object_or_404(Quote, id=int(quote_id))
        value = int(value)

        vote_obj, created = Vote.objects.get_or_create(
            quote=quote, user=request.user, defaults={"value": value}
        )

        if not created:
            vote_obj.value = value
            vote_obj.save()

        data = {"likes": quote.likes_count(), "dislikes": quote.dislikes_count()}
        return JsonResponse(data)
    return JsonResponse({"error": "Invalid request"}, status=400)


def index(request):
    quotes = list(Quote.objects.all())

    weights = [q.weight for q in quotes]

    if quotes:
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
            "index.html",
            context={
                "quote": quote,
                "views": views,
                "text": text,
                "likes": likes,
                "dislikes": dislikes,
                "source": source,
                "creator": creator,
            },
        )
    else:
        return render(request, "index.html", {"quotes": quotes})


class PopularListView(generic.ListView):
    model = Quote
    context_object_name = "top_5_quotes"
    template_name = "most_popular.html"

    def get_queryset(self):
        return Quote.objects.annotate(
            likes_total=Count("votes", filter=Q(votes__value=1))
        ).order_by("-likes_total")[:5]

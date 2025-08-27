from django.shortcuts import render
from django.views import generic
from django.db.models import Count, Q
from .models import Quote
import random

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
    creator = quote.creator.nickname

    return render(
        request,
        'index.html',
        context={'views': views, 'text': text, 'likes': likes, 'dislikes': dislikes, 'source': source, 'creator': creator},
    )

class PopularListView(generic.ListView):
    model = Quote
    context_object_name = 'top_5_quotes'
    template_name = 'most_popular.html'

    def get_queryset(self):
        return Quote.objects.annotate(
            likes_total=Count('votes', filter=Q(votes__value=1))
        ).order_by('-likes_total')[:5]


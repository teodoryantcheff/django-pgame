from django.views import generic
from news.models import NewsEntry

NEWS_LIST_NUM = 5

# Create your views here.
class NewsSummaryView(generic.ListView):
    template_name = 'news/summary.html'
    context_object_name = 'news_summaries'

    def get_queryset(self):
        return NewsEntry.published.all()[:NEWS_LIST_NUM]


class NewsDetailView(generic.DetailView):
    template_name = 'news/detail.html'
    model = NewsEntry

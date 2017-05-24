from django.views.generic import DetailView
from django.views.generic import ListView
from django.db.models import Sum, Count
from django.db.models import F

from api.models import Match, Player, MatchPlayerResults


class MatchListView(ListView):

    model = Match
    template_name = 'match_list.html'
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super(MatchListView, self).get_context_data(**kwargs)
        context['total_time_played'] = Match.objects.aggregate(Sum('duration'))['duration__sum']
        return context

    def get_template_names(self):
        return self.template_name


class PlayerListView(ListView):

    model = Player
    template_name = 'player_list.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerListView, self).get_context_data(**kwargs)
        context["races"] = set(MatchPlayerResults.objects.all().values_list('race', flat=True))
        return context

    def get_template_names(self):
        return self.template_name


class MatchDetailView(DetailView):

    model = Match
    template_name = 'match_details.html'

    def get_context_data(self, **kwargs):
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        context['results'] = MatchPlayerResults.objects.filter(match=self.object)
        return context


class PlayerDetailView(DetailView):

    model = Player
    template_name = 'player_details.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        context['matches'] = self.object.get_matches()
        context['solo_matches'] = self.object.get_solo_matches()
        return context

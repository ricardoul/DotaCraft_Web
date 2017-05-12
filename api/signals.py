from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import MatchPlayerResults, Match


@receiver(post_save, sender=Match, dispatch_uid="update_match_count")
def impact_winrate(sender, instance, **kwargs):
    for result in MatchPlayerResults.objects.filter(match=instance).select_related():
        result.player.matches += 1
        is_solo = result.is_solo()
        if is_solo:
            result.player.solo_matches += 1
        if result.match.winner == result.team:
            result.player.wins += 1
            if is_solo:
                result.player.solo_wins += 1
        result.player.save()

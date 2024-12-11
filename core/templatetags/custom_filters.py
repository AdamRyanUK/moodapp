from django import template

register = template.Library()

@register.filter
def mood_score_color(mood_score):
    red = 255 - (mood_score * 25)
    green = 255 - ((10 - mood_score) * 25)
    return f'rgb({red},{green},0)'

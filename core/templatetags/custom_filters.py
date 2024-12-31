from django import template

register = template.Library()

@register.filter
def mood_score_color(mood_score):
    red = 255 - (mood_score * 25)
    green = 255 - ((10 - mood_score) * 25)
    return f'rgb({red},{green},0)'

@register.filter
def duration_in_hours_minutes(value):
    if value:
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    return value


from django import template
from ..models import Guardia



register = template.Library()

@register.inclusion_tag('core/tags/portada.html')
def guardias_profile(id=1):
    perfiles_guardias = Guardia.objects.filter(get_guardias__id=id)
    return {'perfiles_guardias': perfiles_guardias}




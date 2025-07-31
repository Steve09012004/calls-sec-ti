from django import template

register = template.Library()

@register.simple_tag
def mensagens_nao_lidas(chamado, user):
    return chamado.mensagens_chamado.filter(visualizado=False).exclude(usuario=user).count()

from django import template

register = template.Library()

CENSORED = ['мат', 'материшинник']


@register.filter(name='censor')
def censor(value):
    text = value.split()
    for word in text:
        if word.lower() in CENSORED:
            value = value.replace(word, '****')
    return value
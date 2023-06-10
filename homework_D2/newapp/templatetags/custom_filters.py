from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    censored_words = ['плохое_слово_1', 'нежелательное_слово2', 'нежелательное_слово3']
    censored_value = value

    for word in censored_words:
        censored_value = censored_value.replace(word, '*' * len(word))

    return censored_value
from .models import *
from modeltranslation.translator import register, TranslationOptions

@register(Category)
class CategoryTranlstion(TranslationOptions):
    fields = ('name',)

@register(Post)
class PostTranslation(TranslationOptions):
    fields = ('head', 'text',)

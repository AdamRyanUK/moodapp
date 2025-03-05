# blog/models.py
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.images.models import Image

# Page individuelle pour un article

# Page d'index pour lister les articles
class BlogIndexPage(Page):
    intro = RichTextField(blank=True, help_text="Introduction pour la page du blog")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogposts = self.get_children().live().order_by('-first_published_at')
        context['blogposts'] = blogposts
        return context

from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel  # ✅ C'est bien ici que FieldPanel doit être importé
from wagtail.images.models import Image  # ✅ On importe Image correctement
from wagtail.search import index

class BlogPage(Page):
    date = models.DateField("Date de publication", auto_now_add=True)
    intro = models.CharField(max_length=500, help_text="Résumé de l'article")  
    body = RichTextField(features=['bold', 'italic', 'link', 'image', 'h2', 'h3', 'ol', 'ul'], help_text="Contenu détaillé de l'article")  

    header_image = models.ForeignKey(
        Image, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name="+",
        help_text="Image principale de l'article"
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = [
        FieldPanel("header_image"),  # ✅ Ici c'est enfin correct !
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

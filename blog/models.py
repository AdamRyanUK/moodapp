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

from wagtail.blocks import StructBlock, RichTextBlock, RawHTMLBlock, URLBlock
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.search import index

from wagtail.blocks import StructBlock, CharBlock

class ScriptBlock(StructBlock):
    script_url = CharBlock(help_text="Provide the relative path to your JavaScript file (e.g., 'js/quiz.js')")

    class Meta:
        icon = "code"
        label = "Custom Script Block"


class BlogPage(Page):
    date = models.DateField("Date de publication", auto_now_add=True)
    intro = models.CharField(max_length=500, help_text="Résumé de l'article")
    body = StreamField([
        ('rich_text', RichTextBlock(features=['bold', 'italic', 'link', 'image', 'h2', 'h3', 'ol', 'ul'])),
        ('html', RawHTMLBlock()),
        ('script', ScriptBlock()),  # Add a block for embedding custom scripts
    ], use_json_field=True)

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

    content_panels = Page.content_panels + [
        FieldPanel("header_image"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

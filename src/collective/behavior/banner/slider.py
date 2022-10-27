# -*- coding: utf-8 -*-
from collective.behavior.banner import _
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer


class ISlider(model.Schema):

    model.fieldset(
        'slider',
        label=u"Slider",
        fields=[
            'slider_relation',
        ]
    )

    slider_relation = RelationList(
        title=_(u"Slider Banners"),
        description=_(u"These banners will be used in the slider"),
        default=[],
        value_type=RelationChoice(
            vocabulary='plone.app.vocabularies.Catalog',
        ),
        required=False,
    )
    directives.widget(
        'slider_relation',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': ['Image'],
            'basePath': make_relation_root_path,
        }
    )

alsoProvides(ISlider, IFormFieldProvider)


@implementer(ISlider)
@adapter(IDexterityContent)
class Slider(object):

    def __init__(self, context):
        self.context = context

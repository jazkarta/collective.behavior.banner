# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFPlone.browser.ploneview import Plone
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.behavior.banner.banner import IBanner
from collective.behavior.banner.browser.controlpanel import \
    IBannerSettingsSchema
from collective.behavior.banner.slider import ISlider
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets import ViewletBase
from plone.registry.interfaces import IRegistry
from six.moves.urllib.parse import urlparse
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import getUtility

import random


class BannerViewlet(ViewletBase):
    """ A viewlet which renders the banner """

    banner_template = ViewPageTemplateFile('banner.pt')
    slider_template = ViewPageTemplateFile('slider.pt')

    def render(self):
        if '@@edit' in self.request.steps:
            return ''
        return self.index()

    def index(self):
        context = aq_inner(self.context)
        if ISlider.providedBy(context):
            sliders = self.random_banner
            if sliders and len(sliders) > 1:
                return self.slider_template()
        return self.banner_template()

    def find_banner(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IBannerSettingsSchema)
        types = settings.types
        context = aq_inner(self.context)
        # first handle the obj itself
        if IBanner.providedBy(context):
            if context.banner_hide:
                return False
            banner = self.banner(context)
            if banner:
                return banner
            if context.banner_stop_inheriting:
                return False
            # if all the fields are empty and inheriting is not stopped
        if context.portal_type not in types:
            return False
        context = context.__parent__

        # we walk up the path
        for item in context.aq_chain:
            if IBanner.providedBy(item):
                # we have a banner. check.
                if item.banner_stop_inheriting:
                    return False
                banner = self.banner(item)
                if banner:
                    return banner
            if INavigationRoot.providedBy(item):
                return False
            if item.portal_type not in types:
                return False

        return False

    def banner(self, obj):
        """ return banner of this object """
        banner = {}
        image = getattr(obj, 'banner_image', False)
        if image:
            if hasattr(image, 'to_object'):
                to_obj = image.to_object
                if to_obj:
                    banner['banner_image'] = to_obj
            else:
                banner['banner_image'] = '%s/@@images/banner_image' \
                    % obj.absolute_url()
        if obj.banner_title:
            banner['banner_title'] = obj.banner_title
        if obj.banner_description:
            crop = Plone(self.context, self.request).cropText
            banner['banner_description'] = crop(obj.banner_description, 400)
        if obj.banner_text:
            banner['banner_text'] = obj.banner_text.output
        if obj.banner_link:
            to_obj = obj.banner_link.to_object
            if to_obj:
                banner['banner_link'] = to_obj.absolute_url()
                banner['banner_linktext'] = to_obj.Title()
        if obj.banner_linktext:
            banner['banner_linktext'] = obj.banner_linktext
        if obj.banner_fontcolor:
            banner['banner_fontcolor'] = obj.banner_fontcolor
        if obj.banner_url:
            banner['banner_url'] = obj.banner_url
        return banner

    @lazy_property
    def random_banner(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IBannerSettingsSchema)
        types = settings.types
        context = aq_inner(self.context)
        # first handle the obj itself
        if ISlider.providedBy(context):
            if context.banner_hide:
                return False
            slider = context.slider_relation
            if not slider and context.banner_stop_inheriting:
                return False
            # if all the fields are empty and inheriting is not stopped
        if context.portal_type not in types:
            return False
        if not slider:
            context = context.__parent__
            # we walk up the path
            for item in context.aq_chain:
                if ISlider.providedBy(item):
                    # we have a banner. check.
                    if item.banner_stop_inheriting:
                        return False
                    slider = item.slider_relation
                    if slider:
                        break
                if INavigationRoot.providedBy(item):
                    return False
                if item.portal_type not in types:
                    return False
        banners = []
        raw_banners = slider
        for banner in raw_banners:
            if banner.to_object:
                banners.append(banner.to_object)

        self.scroll = len(banners) > 1

        random.shuffle(banners)
        return banners

    def getVideoEmbedMarkup(self, url):
        """ Build an iframe from a YouTube or Vimeo share url """
        # https://www.youtube.com/watch?v=Q6qYdJuWB6w
        YOUTUBE_TEMPLATE = '''
            <iframe
                width="660"
                height="495"
                src="//www.youtube-nocookie.com/embed/{1}?showinfo=0"
                frameborder="0"
                allowfullscreen>
            </iframe>
        '''
        # https://vimeo.com/75721023
        VIMEO_TEMPLATE = '''
            <iframe
                src="//player.vimeo.com/video/{0}?title=0&amp;byline=0&amp;portrait=0"
                width="660"
                height="371"
                frameborder="0"
                webkitallowfullscreen
                mozallowfullscreen
                allowfullscreen>
            </iframe>
        '''
        try:
            parsed = urlparse(url)
        except AttributeError:
            return ''
        path = parsed.path.replace('/', '')
        videoId = parsed.query.replace('v=', '')
        if 'youtube' in parsed.netloc:
            template = YOUTUBE_TEMPLATE
        elif 'youtu.be' in parsed.netloc:
            videoId = path
            template = YOUTUBE_TEMPLATE
        elif 'vimeo' in parsed.netloc:
            template = VIMEO_TEMPLATE
        else:
            return ''
        # It so happens that path is needed by the Vimeo format,
        # while videoId is needed by the Youtube format, so only one
        # of the variables will have a useful value, depending on the player.
        # Each template will use the argument it cares about and ignore the
        # other.
        return template.format(path, videoId)


class BackgroundViewlet(ViewletBase):
    """ A viewlet which renders the background """

    def render(self):
        if '@@edit' in self.request.steps:
            return ''
        return self.index()

    def find_background(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IBannerSettingsSchema)
        types = settings.types
        context = aq_inner(self.context)
        # first handle the obj itself
        if IBanner.providedBy(context):
            background = self.background(context)
            if background:
                return background
            # if all the fields are empty and inheriting is not stopped
        if context.portal_type not in types:
            return False
        context = context.__parent__

        # we walk up the path
        for item in context.aq_chain:
            if IBanner.providedBy(item):
                # we have a banner. check.
                background = self.background(item)
                if background:
                    return background
            if INavigationRoot.providedBy(item):
                return False
            if item.portal_type not in types:
                return False

        return False

    def background(self, obj):
        """ return background of this object """
        image = getattr(obj, 'banner_header_image', False)
        if image:
            if hasattr(image, 'to_object'):
                to_obj = image.to_object
                if to_obj:
                    return to_obj

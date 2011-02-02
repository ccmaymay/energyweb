def media_url(request):
    '''
    Return the URL used for site media.
    '''
    from django.conf import settings
    return {'media_url': settings.MEDIA_URL}

def nav_urls(request):
    '''
    Return URLs used in generating the navigation bar.
    '''
    from django.core.urlresolvers import reverse
    return {'dynamic_graph_url': reverse('energyweb.graph.views.dynamic_graph'),
            'static_graph_url': reverse('energyweb.graph.views.static_graph'),
            'data_interface_url': reverse('energyweb.graph.views.data_interface')}

def media_url(request):
    from django.conf import settings
    return {'media_url': settings.MEDIA_URL}

def nav_urls(request):
    from django.core.urlresolvers import reverse
    return {'graph_url': reverse('graph.views.index'),
            'static_graph_url': reverse('graph.views.static_graph'),
            'data_interface_url': reverse('graph.views.data_interface')}

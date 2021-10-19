from django.template import Library

register = Library()


@register.simple_tag()
def get_filter_params(request):
    params = request.GET
    completed_list = []

    for param in params.keys():

        if params[param]:
            completed_list.append(f'{param}={params[param]}&')

    return completed_list
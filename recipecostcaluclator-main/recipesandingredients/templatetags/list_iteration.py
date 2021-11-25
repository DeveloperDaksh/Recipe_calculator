from django.template.defaulttags import register


@register.filter
def iterate_list(given_list):
    final_str = ''
    for each in given_list[1:-1].split(','):
        final_str += each.strip()[1:-1] + ' ,'
    return final_str[:-1]

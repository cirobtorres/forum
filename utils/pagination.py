from django.core.paginator import Paginator


def pagination_func(request, object_parse, per_page) -> list:
    current_page = int(request.GET.get('page', 1))
    paginator = Paginator(object_list=object_parse, per_page=per_page)
    page_obj = paginator.get_page(current_page)
    num_pages = paginator.page_range
    last_page = paginator.num_pages
    next_page_exists = page_obj.has_next()
    previous_page_exists = page_obj.has_previous()
    total_elements = paginator.count
    return [
        page_obj, num_pages, next_page_exists, previous_page_exists, 
        last_page, current_page, total_elements,
        ]

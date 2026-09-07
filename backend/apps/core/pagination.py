def paginate(queryset, request, default_size=12, max_size=48):
    try:
        page = max(1, int(request.query_params.get("page", 1)))
    except (TypeError, ValueError):
        page = 1
    try:
        size = int(request.query_params.get("page_size", default_size))
    except (TypeError, ValueError):
        size = default_size
    size = max(1, min(size, max_size))

    total = queryset.count()
    start = (page - 1) * size
    items = list(queryset.skip(start).limit(size))
    return items, {
        "page": page,
        "page_size": size,
        "total": total,
        "pages": (total + size - 1) // size or 1,
    }

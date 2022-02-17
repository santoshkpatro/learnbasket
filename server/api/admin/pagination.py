from rest_framework import pagination


class DefaultPagination(pagination.LimitOffsetPagination):
    max_limit = 100
from rest_framework.pagination import PageNumberPagination


class VideoPagination(PageNumberPagination):
    page_size = 12


class CommentPagination(PageNumberPagination):
    page_size = 15

from django.conf import settings

from django.urls import include, path

from hw_11.views import *

urlpatterns = [
    path('', home),  # noqa: F405
    path('authors/', authors, name='authors'),  # noqa: F405
    path('authors/<int:pk>', authors_info, name='author-detail'),  # noqa: F405
    path('books/', books, name='books'),  # noqa: F405
    path('books/<int:pk>', book_info, name='book-detail'),  # noqa: F405
    path('publishers/', publishers, name='publishers'),  # noqa: F405
    path('publishers/<int:pk>', publisher_info, name='publisher-detail'),  # noqa: F405
    path('store/', store, name='stores'),  # noqa: F405
    path('store/<int:pk>', store_info, name='store-detail'),  # noqa: F405
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

from django.conf import settings

from django.urls import include, path

from hw_11 import views
from hw_11.views import *

urlpatterns = [
    path('', home),  # noqa: F405
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('books/', books, name='books'),  # noqa: F405
    path('books/<int:pk>', book_info, name='book-detail'),  # noqa: F405
    path('publishers/', publishers, name='publishers'),  # noqa: F405
    path('publishers/<int:pk>', publisher_info, name='publisher-detail'),  # noqa: F405
    path('store/', store, name='stores'),  # noqa: F405
    path('store/<int:pk>', store_info, name='store-detail'),  # noqa: F405
    path('celery/', celery, name='celery'),

    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

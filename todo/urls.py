from django.urls import path

from .views import (
    itemHomeListView,
    itemCreateView,
    itemRemoveView,
    itemCompleteView,
)


urlpatterns = [
    path('', itemHomeListView, name='home'),
    path('new/', itemCreateView, name='new'),
    path('<uuid:item_id>/remove', itemRemoveView, name='remove'),
    path('<uuid:item_id>/complete', itemCompleteView, name='complete')

]

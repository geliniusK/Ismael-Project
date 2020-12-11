from django.urls import path

from .views import (
    itemAddListView,
    itemCreateView,
    itemRemoveView,
    itemCompleteView,
    )


urlpatterns = [
    path('', itemAddListView, name='home'),
    path('new/', itemCreateView, name='new'),
    path('<uuid:item_id>/remove', itemRemoveView, name='remove'),
    path('<uuid:item_id>/complete', itemCompleteView, name='complete')

]

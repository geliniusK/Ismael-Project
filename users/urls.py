from django.urls import path

from .views import (
    SignupPageView,
    UserSearchView,
    UserDetailView,
    FollowingListView,
    FollowersListView,
    followUser,
    unfollowUser
    )

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('search/', UserSearchView.as_view(), name='user_search'),
    path('<uuid:pk>', UserDetailView.as_view(), name='profile'),
    path('<uuid:object_id>/follow', followUser, name='follow'),
    path('<uuid:object_id>/unfollow', unfollowUser, name='unfollow'),
    path('following/', FollowingListView.as_view(), name='following_list'),
    path('followers/', FollowersListView.as_view(), name='followers_list'),
]

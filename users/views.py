from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from .forms import CustomUserCreationForm


class SignupPageView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserSearchView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return get_user_model().objects.filter(username__icontains=query).exclude(username=self.request.user)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_profile.html'


class FollowingListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'following_list.html'

    def get_queryset(self):
        return self.request.user.friends.all()


class FollowersListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'followers_list.html'

    def get_queryset(self):
        return get_user_model().objects.filter(friends=self.request.user)


@login_required()
def followUser(request, object_id):
    u1 = request.user
    u2 = get_user_model().objects.get(id=object_id)
    u1.friends.add(u2)
    u2.new_f.add(u1)
    u1.save()

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


@login_required()
def unfollowUser(request, object_id):
    u1 = request.user
    u2 = get_user_model().objects.get(id=object_id)
    u1.friends.remove(u2)
    u1.save()

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


# Create your views here.

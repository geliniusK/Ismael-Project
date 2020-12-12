from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import ItemForm
from .models import Item
from django.contrib import messages




@login_required()
def itemAddListView(request):

    u = request.user
    if u.new_f.all():
        for msg in u.new_f.all():
            messages.add_message(request, 60, f'{msg} is now following you')
        u.new_f.clear()


    context = {
    'item_list': Item.objects.filter(author=request.user).exclude(visible_priv=False),
    'us': get_user_model().objects.order_by('-score')[:5],
    'item_public': Item.objects.filter(author__in=request.user.friends.all(), public=True).order_by('-share_time')[:5],
    'form': ItemForm(request.POST)
    }

    return render(request, 'home.html', context)


def itemCreateView(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            new_entry = Item(description=form.cleaned_data['item'], author_id=request.user.id)
            new_entry.save()
            return redirect('home')
    else:
        form = ItemForm(request.POST)
    return render(request, 'home.html', {'form': form})


def itemRemoveView(request, item_id):
    if request.method == 'POST':
        x = Item.objects.get(pk=item_id)
        x.visible_priv = False
        x.save()
    return redirect("home")


def itemCompleteView(request, item_id):
    if request.method == 'POST':
        x = Item.objects.get(pk=item_id)
        request.user.score += 1
        request.user.save()

        if bool(request.POST.get('share')):
            x.share_time = timezone.now()
            x.public = True

        x.visible_priv = False
        x.save()

    return redirect("home")
# Create your views here.

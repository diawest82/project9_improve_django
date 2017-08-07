from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .forms import *


def menu_list(request):
    all_menus = Menu.objects.all().prefetch_related('items')
    menus = all_menus.filter(expiration_date__gte=timezone.now()
                             ).order_by(
        'expiration_date'
    )
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try:
        item = Item.objects.select_related('chef').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            form.save_m2m()
            return redirect('menu:menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/new_menu.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    items = Item.objects.all()
    form = ChangeMenuForm(instance=menu)
    if request.method == 'POST':
        form = ChangeMenuForm(request.POST, instance=menu)
        menu = form.save(commit=False)
        menu.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('menu:menu_list'))

    return render(request, 'menu/change_menu.html', {
        'form': form,
        'menu': menu,
        'items': items
    })

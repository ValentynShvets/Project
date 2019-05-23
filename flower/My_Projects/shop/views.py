from pprint import pprint

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, render_to_response
from django.template.context_processors import csrf
from django.views import generic
from .models import *
from django import forms
# from allauth.account.forms import LoginForm
# from allauth.account.forms import SignupForm
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.views.generic import TemplateView, FormView
from django.contrib.sessions import base_session


class TopGoodsCookiesMixin():
    # template_name = "index.html"
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['top_goods'] = Good.objects.all()[:6]
        quantity = 0
        summa = 0
        for item in self.request.session.keys():
            if 'good_' in item:
                q = int(self.request.session.get(item))
                try:
                    quantity += q
                    summa += q * Good.objects.get(pk=int(item[5:])).price
                except:
                    pass
        context['total_quantity'] = quantity
        context['sum'] = summa
        context['user_id'] = self.request.user.id
        try:
            context['top_reviews'] = Good.objects.get(pk=self.kwargs['pk']).reviews_set.all()[:3]
        except:
            pass
        context['order'] = False
        context['sum_and_send'] = summa + 500
        return context


# def base(request):
#     def wrapper(func, *args, **kwargs):
#
#         quantity = 0
#         total = 0
#         func()
#         for key in request.session.keys():
#             print(key)
#             if "good_" not in key:
#                 continue
#             good = Good.objects.get(pk=int(key[5:]))
#             quantity += request.session[key]
#             total += good.price * request.session[key]
#
#         return func({'total_quantity': quantity, 'sum': total})
#
#     return wrapper


def main_view(request):
    total = 0
    quantity = 0
    all_goods = Good.objects.all()
    context = {'top_goods': Good.objects.all()}
    page = request.GET.get('page')
    all_pages = Paginator(all_goods, 6)
    if page is None:
        page = all_pages.get_page(1)
    elif int(page) > all_pages.num_pages:
        page = all_pages.num_pages
    pages = all_pages.get_page(page)
    # total_quontity = request.session[good_key]
    print(request.session.keys())
    for key in request.session.keys():
        print(key)
        if "good_" not in key:
            continue
        good = Good.objects.get(pk=int(key[5:]))
        quantity += request.session[key]
        total += good.price * request.session[key]
        print(good.price * request.session[key])
    return render(request, "index.html", {'total_quantity': quantity, 'sum': total, 'top_goods': pages, "page": page,
                                          'end_page': all_pages.num_pages})


def details(request, pk):
    print(pk)
    quantity = 0
    total = 0
    context = {'good': Good.objects.get(id=pk),
               'top_reviews': Reviews.objects.filter(good_id=pk)[:5],
               'count_reviews': Reviews.objects.filter(good_id=pk),
               'top_goods': Good.objects.all()}
    print(context['top_goods'])
    try:
        context['reviews'] = Reviews.objects.get(good_id=pk)
    except:
        pass
    for key in request.session.keys():
        print(key)
        if "good_" not in key:
            continue
        good = Good.objects.get(pk=int(key[5:]))
        quantity += request.session[key]
        total += good.price * request.session[key]
        context['total_quantity'] = quantity
        context['sum'] = total
    return render(request, "shop/detail.html", context)


def rewiews(request):
    args = {}

    if request.POST:
        text = request.POST.get("text", "")
        url = request.POST.get("url", "")

        if text:
            good_id = request.POST.get("good", "")
            user_id = request.POST.get("user", "")
            Reviews(good_id=good_id, user_id=user_id, text=text).save()
            return redirect(url)

        else:
            args['messages'] = "Введіть відгук"
            messages.success(request, "Напишіть ваш відгук")
            return redirect(url)


def all_reviews(request, pk):
    context = {'good': Good.objects.get(id=pk),
               'top_reviews': Reviews.objects.filter(good_id=pk),
               'top_goods': Good.objects.all()}
    try:
        context['reviews'] = Reviews.objects.get(good_id=pk)
    except:
        pass

    return render(request, "shop/all_reviews.html", context)


def user_registration(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()

    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = authenticate(username=newuser_form.cleaned_data['username'],
                                   password=newuser_form.cleaned_data['password2'], )
            login(request, newuser)
            return redirect("/")
        else:
            args['form'] = newuser_form
    return render_to_response("shop/registration.html", args)


def user_login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            args['login_error'] = "Користувач не знайдений"
            return render_to_response('shop/login.html', args)
    else:
        return render_to_response("shop/login.html", args)


def user_logout(request):
    logout(request)
    return redirect("/")


def waranty(request):
    return render(request, "shop/waranty.html")


def contacts(request):
    return render(request, "shop/contacts.html")


class GoodsList(TopGoodsCookiesMixin, generic.ListView):
    model = Good
    paginate_by = 2


class GoodDetail(TopGoodsCookiesMixin, generic.DetailView):
    model = Good

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.GET.get('q'):
            self.request.session['good_' + str(self.kwargs['pk'])] = int(self.request.GET.get('q'))
        context = super().get_context_data(object_list=None, **kwargs)
        context['quantity'] = self.request.session.get('good_' + str(self.kwargs['pk']), 1)

        return context


#
# class Reviewss(LoginRequiredMixin, generic.CreateView):
#     model = Reviews
#     form_class = ReviewForm
#
#     def get_form_kwargs(self):
#         kwargs = super(Reviewss, self).get_form_kwargs()
#         print(kwargs)
#         self.success_url = kwargs['data']['url']
#         return kwargs
#
#     def form_invalid(self, form):
#         messages.success(self.request, "Ніпишіть ваш відгук")
#         return redirect(self.success_url)


def show_order(request, pk):
    properties_from_order = list(('name', 'price', 'quantity',))
    goods_in_order = GoodsInOrder.objects.filter(order_id=pk). \
        values_list('good__name', 'good__price', 'quantity')
    rez = [dict(zip(properties_from_order, i)) for i in list(goods_in_order)]
    return JsonResponse(rez, safe=False)


class BasketShow(TopGoodsCookiesMixin, generic.TemplateView):
    template_name = "shop/basket.html"

    def get_context_data(self, **kwargs):
        context = super(BasketShow, self).get_context_data(**kwargs)
        goods = []
        total_sum = 0
        for good_key in self.request.session.keys():
            if 'good_' not in good_key: continue
            good = Good.objects.get(pk=int(good_key[5:]))
            summ = good.price * int(self.request.session[good_key])
            total_sum += summ
            goods.append((good, int(self.request.session[good_key]), summ))
        context['goods'] = goods
        context['total_summ'] = total_sum
        context['order'] = True
        return context


def basket(request):
    context = {}
    goods = []
    total = 0
    for key in request.session.keys():
        if 'good_' not in key:
            continue

        if int(request.session[key]) == 0:
            continue

        good = Good.objects.get(pk=int(key[5:]))
        summ = good.price * int(request.session[key])
        total += summ
        goods.append((good, int(request.session[key]), summ))
    context['top_goods'] = Good.objects.all()
    context['goods'] = goods
    context['total'] = total
    context['order'] = True
    return render(request, "shop/basket.html", context)


def add_to_basket(request, pk):
    # url = request.POST.get("url", "")
    good = 'good_' + str(pk)
    print(request.POST.get('q', ''))
    url = request.GET.get('url','')
    print(url)
    if request.POST:
        q = request.POST.get('q', '')
        quantity = request.session.get(good, 0) + int(q)
        request.session[good] = quantity
        return redirect(f"/{pk}")
    quantity = request.session.get(good, 0) + int(request.GET.get('q'))
    request.session[good] = quantity
    if url:
        return redirect(f'/{url}')

    return redirect("/")


def order(request):
    context = {}
    goods = []
    total = 0
    quantity = 0
    for good_key in request.session.keys():
        if 'good_' not in good_key: continue
        if int(request.session[good_key]) == 0:
            continue
        good = Good.objects.get(pk=int(good_key[5:]))
        summ = good.price * int(request.session[good_key])
        # total += summ
        goods.append((good, int(request.session[good_key]), summ))
    context['top_goods'] = Good.objects.all()
    context['goods'] = goods
    context['total'] = total
    context['order'] = True
    for key in request.session.keys():
        if "good_" not in key:
            continue

        good = Good.objects.get(pk=int(key[5:]))
        quantity += request.session[key]
        total += good.price * request.session[key]
        context['total_quantity'] = quantity
        context['sum'] = total
    context['total_and_shipping'] = total + 150
    return render(request, 'shop/order.html', context)


def order_confirm(request):
    if request.POST:
        if not request.user.id:
            return redirect("shop:register")
        total = 0
        quantity = 0
        key_list = request.session.keys()
        for key in key_list:

            if "good_" not in key:
                continue
            good = Good.objects.get(pk=int(key[5:]))
            quantity += request.session[key]

            total += good.price * request.session[key]
        surname = request.POST.get("surname", "")
        name = request.POST.get("name", "")
        lastname = request.POST.get("lastname", "")
        phone = request.POST.get("phone", "")
        city = request.POST.get("city", "")
        street = request.POST.get("street", "")
        text = request.POST.get("text", "")
        date = request.POST.get("date", "")
        time = request.POST.get("time", "")
        card = request.POST.get("card", "")
        if not surname or not name or not phone or not city or not street or not date or not time:
            messages.success(request, "Заповніть необхідні поля")
            return redirect("shop:order")
        else:
            total += 150
            date_time = str(date) + " " + str(time)
            Order(receiver_surname=surname, receiver_name=name, receiver_lastname=lastname,
                  phone=phone, address_city=city, address_local=street, shipping_date=date_time, receiver_text=text,
                  sum_total=total, user_id=int(request.user.id)).save()
            orders = Order.objects.last()
            for key in list(request.session.keys()):

                if "good_" not in key:
                    continue
                ids = int(str(key).replace('good_', ""))
                print(ids)
                GoodsInOrder(good_id=ids, order_id=orders.id, quantity=quantity).save()
                # request.session.r
                del request.session[key]
            # if request.session.clear():

            messages.success(request, "Замовлення успішно зроблено")

            return redirect("shop:order")


def status(request):
    statuses = {'statuses': Order.objects.filter(user_id=request.user.id)[::-1]}

    return render(request, 'shop/status.html', statuses)


# class AllReviews(LoginRequiredMixin, generic.CreateView):
#     model = Reviews
#     form_class = ReviewForm
#
#     def get_form_kwargs(self):
#         kwargs = super(AllReviews, self).get_form_kwargs()
#         print(kwargs)
#         # print(kwargs['data']['url'])
#         # self.success_url = kwargs['data']['url']
#
#         # self.success_url = f"/{self.kwargs['pk']}"
#         return kwargs
#
#     def form_invalid(self, form):
#         messages.success(self.request, "Ніпишіть ваш відгук")
#         return redirect(self.success_url)




def remove(request):
    request.session.pop(request.GET.get('remove'))
    return redirect('shop:basket')

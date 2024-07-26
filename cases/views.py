from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import ListView, DetailView

from .models import Case, CaseOrder, CaseOrderItem
from .forms import AddToCart, OrderForm
from .cart import Cart


# --------------------------------- Case Views ---------------------------------
class CaseListView(ListView):
    model = Case
    queryset = Case.objects.all()
    paginate_by = 8
    context_object_name = 'cases'
    template_name = 'cases/case_list.html'


class CaseDetailView(DetailView):
    model = Case
    template_name = 'cases/case_detail.html'
    context_object_name = 'case'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_to_cart_form'] = AddToCart()
        return context


# --------------------------------- Cart Views ---------------------------------
def cart_detail_view(request):
    cart = Cart(request)
    for item in cart:
        item['case_update_meter_form'] = AddToCart(initial={
            'meter': item['meter'],
            'inplace': True,
        })
    context = {
        'cart': cart,
    }
    return render(request, 'cases/cart_detail.html', context)


def add_to_cart_view(request, case_id):
    cart = Cart(request)
    case = get_object_or_404(Case, id=case_id)
    form = AddToCart(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        meter = cleaned_data['meter']
        cart.add(case, meter, replace_current_meter=cleaned_data['inplace'])
    return redirect('cart_detail')


def remove_from_cart_view(request, case_id):
    cart = Cart(request)
    case = get_object_or_404(Case, id=case_id)
    cart.remove(case)
    return redirect('cart_detail')


@require_POST
def cart_clear(request):
    cart = Cart(request)
    if len(cart):
        cart.clear()
        messages.success(request, 'سبد با موفقیت خالی شد')
    else:
        messages.warning(request, 'سبد شما خالی است')
    return redirect('cart_empty')


def cart_empty_view(request):
    return render(request, 'cases/cart_empty.html')


# --------------------------------- Order Views ---------------------------------
def order_create_view(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, 'سبد خرید شما خالی است، ابتدا محصولی به آن اضافه کنید')
        return redirect('case_list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                case = item['case_obj']
                CaseOrderItem.objects.create(
                    order=order_obj,
                    case=case,
                    meter=item['meter'],
                    base_value=case.base_value,
                )
            cart.clear()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()
            messages.success(request, 'سفارش شما با موفقیت ثبت شد')
            order_form = OrderForm()
            request.session['order_id'] = order_obj.id
            return redirect('case_list')

    context = {
        'cart': cart,
        'form': order_form,
    }
    return render(request, 'cases/order_create.html', context)



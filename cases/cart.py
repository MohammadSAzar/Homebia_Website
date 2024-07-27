from .models import Case

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, case, meter=1, replace_current_meter=False):
        case_id = str(case.id)
        if case_id not in self.cart:
            self.cart[case_id] = {'meter': 0}
        if replace_current_meter:
            self.cart[case_id]['meter'] = meter
        else:
            self.cart[case_id]['meter'] += meter
        self.save()

    def remove(self, case):
        case_id = str(case.id)
        if case_id in self.cart:
            del self.cart[case_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        case_ids = self.cart.keys()
        cases = Case.objects.filter(id__in=case_ids)
        cart = self.cart.copy()
        for case in cases:
            cart[str(case.id)]['case_obj'] = case
        for item in cart.values():
            item['total_price'] = item['meter'] * item['case_obj'].metric_price
            yield item

    def __len__(self):
        return sum(item['meter'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def total_value(self):
        return sum(item['meter'] * item['case_obj'].metric_price for item in self.cart.values())

    def tax(self):
        return sum(int(item['meter'] * item['case_obj'].metric_price * 0.10) for item in self.cart.values())

    def total_value_plus_tax(self):
        return sum(int(item['meter'] * item['case_obj'].metric_price * 1.10) for item in self.cart.values())

    def is_empty(self):
        if self.cart:
            return False
        return True


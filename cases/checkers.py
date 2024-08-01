min_case_metric_price = 10000000  # TOOMAN
max_case_metric_price = 1000000000  # TOOMAN


def case_metric_price_checker(price):
    if min_case_metric_price <= price <= max_case_metric_price:
        return True



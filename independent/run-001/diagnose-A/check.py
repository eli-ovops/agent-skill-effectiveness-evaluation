from orders import cart_total, invoice_total


cases = [(45, None, 55), (45, 0, 45), (45, 8, 53), (100, None, 100), (100, 0, 100), (100, 8, 108)]
failures = []
for entry in (cart_total, invoice_total):
    for subtotal, shipping, expected in cases:
        actual = entry(subtotal, shipping)
        if actual != expected:
            failures.append(f'{entry.__name__}({subtotal}, {shipping}) = {actual}; expected {expected}')

print(f'{len(cases) * 2 - len(failures)}/{len(cases) * 2} checks passed')
for failure in failures:
    print(failure)
raise SystemExit(bool(failures))

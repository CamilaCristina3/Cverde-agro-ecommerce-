"""
COVERDE - apps/payments/views.py
Views de pagamento em modo teste (Portugal).
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from apps.orders.models import Order
from apps.users.services import (
    send_new_order_notification_to_producer,
    send_order_confirmation_email,
)


@login_required
def payment_checkout(request, order_id):
    """Página de pagamento (modo teste) - Portugal."""
    order = get_object_or_404(Order, id=order_id, customer=request.user, status='pending')

    if request.method == 'POST':
        method = request.POST.get('payment_method') or request.POST.get('method') or Payment.Method.CARD_TEST
        method = method.strip() or Payment.Method.CARD_TEST

        password = (request.POST.get('test_password') or '').strip()
        signature = (request.POST.get('test_signature') or '').strip()
        credential = (request.POST.get('test_credential') or '').strip()
        if not credential:
            credential = password or signature

        # Criar registo de pagamento
        payment = Payment.objects.create(
            order=order,
            customer=request.user,
            method=method,
            amount=order.total,
            status=Payment.Status.PROCESSING,
            is_test_payment=True,
        )

        success, msg = payment.approve_test_payment(credential)

        if success:
            send_order_confirmation_email(request.user, order, payment)

            for seller_order in order.seller_orders.all():
                if seller_order.store.owner:
                    send_new_order_notification_to_producer(
                        seller_order.store.owner,
                        order,
                        seller_order.store
                    )

            messages.success(
                request,
                'Pagamento de teste aprovado com sucesso. A sua encomenda foi confirmada.'  # ← Portugal
            )
            return redirect('payments:success', payment_id=payment.id)
        else:
            payment.status = Payment.Status.FAILED
            payment.failure_reason = msg
            payment.save(update_fields=['status', 'failure_reason'])
            messages.error(request, f'Pagamento não aprovado: {msg}')

    # Métodos de pagamento adaptados para Portugal
    payment_methods = [
        {'value': 'mb_way', 'label': 'MB WAY', 'icon': 'fas fa-mobile-alt'},
        {'value': 'multibanco', 'label': 'Referência Multibanco', 'icon': 'fas fa-bank'},
        {'value': 'paypal', 'label': 'PayPal', 'icon': 'fab fa-paypal'},
        {'value': 'card_test', 'label': 'Cartão Teste', 'icon': 'fas fa-credit-card'},
        {'value': 'bank_transfer_test', 'label': 'Transferência Bancária Teste', 'icon': 'fas fa-university'},
    ]

    return render(request, 'payments/checkout.html', {
        'order': order,
        'payment_methods': payment_methods,  # ← Portugal: métodos adaptados
        'test_hint': 'Use a senha 1234 ou a assinatura COVERDE-TEST',
        'title': 'Pagamento'
    })


@login_required
def payment_success(request, payment_id):
    """Página de sucesso do pagamento (Portugal)."""
    payment = get_object_or_404(Payment, id=payment_id, customer=request.user)
    return render(request, 'payments/success.html', {
        'payment': payment,
        'title': 'Pagamento Confirmado'
    })

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.forms import PaymentForm
from apps.models import User, Payment


class PaymentFormView(FormView):
    template_name = "payment/payment.html"
    form_class = PaymentForm
    success_url =  reverse_lazy('payment')


    def form_valid(self, form):

        user_pk = self.request.user.id
        amount_sum = form.cleaned_data.get("transferred_amount")
        balance = User.objects.filter(pk=user_pk).first().balance
        balance = float(balance)-float(amount_sum)
        User.objects.filter(pk=user_pk).update(balance = balance)
        form.save()
        return super().form_valid(form)


    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request,error)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        id_user = self.request.user.id
        data =  super().get_context_data(**kwargs)
        data["user"] = User.objects.filter(pk=id_user).first().balance
        data["payments"] = Payment.objects.filter(user_id=id_user)
        return data




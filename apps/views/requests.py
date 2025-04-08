from django.views.generic import TemplateView

from apps.models import Payment, Order


class RequestTemplateView(TemplateView):
    template_name = "sorov/sorov.html"

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        data["orders"] = Order.objects.filter(owner_id=self.request.user.id)
        return data


class DiagramTemplateView(TemplateView):
    template_name = "sorov/diagram.html"









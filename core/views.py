from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.template.loader import get_template
from core.models import Transaction
from xhtml2pdf.pisa import CreatePDF
from django.http import HttpResponse
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from core.serializers.transaction_serializer import TransactionSerializer


class ListTransactionPdf(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    """
    Generate PDF for Transaction Model

    Args:
        APIView (file): PDF with transaction detail
    """
    queryset = Transaction.objects.all()
    lookup_field = 'transaction_id'

    # TODO fix pdf formatting
    # TODO permission class

    def get(self, request, *args, **kwargs):
        if 'transaction_id' in kwargs:
            return self.retrieve(request, *args, **kwargs)

        template = get_template('core/pdf/all_transaction_list.html')
        transaction_list = self.filter_queryset(self.get_queryset())
        pdf_html = template.render({
            'transactions': transaction_list
        })

        response = HttpResponse(content_type='application/pdf')
        pdf_status = CreatePDF(pdf_html, dest=response)

        if pdf_status.err:
            return Response('Error in generating PDF. Try again', status=400)

        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response

    def retrieve(self, request, *args, **kwargs):
        try:
            template = get_template('core/pdf/transaction_detail.html')
            transaction = self.get_object()

            pdf_html = template.render({
                'transaction': transaction
            })

            response = HttpResponse(content_type='application/pdf')
            pdf_status = CreatePDF(pdf_html, dest=response)

            if pdf_status.err:
                return Response('Error in generating PDF. Try again', status=400)

            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            return response
        except Transaction.DoesNotExist:
            return Response("Transaction Id Not Found", status=404)


class ApproveNewTransaction(UpdateModelMixin, GenericAPIView):
    queryset = Transaction.objects.all()
    lookup_field = 'transaction_id'
    serializer_class = TransactionSerializer

    # TODO permission class

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.transaction_status = True
            instance.save()

            serialzer = self.get_serializer(instance, partial=True)
            return Response(serialzer.data, status=200)
        except Transaction.DoesNotExist:
            return Response("Transaction Id does not exists", status=404)

    def patch(self, request, *args, **kwargs):
        # Note how we use `partial_update()` here
        return self.partial_update(request, *args, **kwargs)

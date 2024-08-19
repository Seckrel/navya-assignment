from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.template.loader import get_template
from core.models import Transaction
from xhtml2pdf.pisa import CreatePDF
from django.http import HttpResponse
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from core.serializers.transaction_serializer import TransactionSerializer
from rest_framework.exceptions import ValidationError
from auths.permissions import IsManagerPermission, IsStaffPermission
from django.conf import settings
import os


class ListTransactionPdf(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    """
    Generate PDF for Transaction Model

    Args:
        APIView (file): PDF with transaction detail
    """
    queryset = Transaction.approved.all()
    lookup_field = 'transaction_id'
    permission_classes = [IsStaffPermission | IsManagerPermission]

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL   
        mRoot = settings.MEDIA_ROOT 

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        """
        Generates PDF with list of approved transactions

        Args:
            request (Request): object of Request class

        Returns:
            Response: PDF file on success
        """
        if 'transaction_id' in kwargs:
            return self.retrieve(request, *args, **kwargs)

        template = get_template('core/pdf/all_transaction_list.html')
        transaction_list = self.filter_queryset(self.get_queryset())
        pdf_html = template.render({
            'transactions': transaction_list
        })

        response = HttpResponse(content_type='application/pdf')
        pdf_status = CreatePDF(pdf_html, dest=response,
                               link_callback=self.link_callback)

        if pdf_status.err:
            return Response('Error in generating PDF. Try again', status=400)

        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response

    def retrieve(self, request, *args, **kwargs):
        """
        Generates PDF file for a single approved transaction

        Args:
            request (Request): object of Request class takes transaction_id as params

        Returns:
            Response: A PDF file with approved transaction detail on success
        """
        try:
            template = get_template('core/pdf/transaction_detail.html')
            transaction = self.get_object()

            pdf_html = template.render({
                'transaction': transaction
            })

            response = HttpResponse(content_type='application/pdf')
            pdf_status = CreatePDF(
                pdf_html, dest=response, link_callback=self.link_callback)

            if pdf_status.err:
                return Response('Error in generating PDF. Try again', status=400)

            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            return response
        except Transaction.DoesNotExist:
            return Response("Transaction Id Not Found", status=404)


class ApproveNewTransaction(UpdateModelMixin, GenericAPIView):
    """
    Allows only Manager level users to change transaction status to either approved | pending | rejected
    Takes transaction_id as params

    Raises:
        ValidationError: Raises Validation exception if this API where to be used to update other fields of Transaction Model   

    Returns:
        Response: JSON containing entire transaction detail
    """
    queryset = Transaction.objects.all()
    lookup_field = 'transaction_id'
    serializer_class = TransactionSerializer
    permission_classes = [IsManagerPermission]

    def update(self, request, *args, **kwargs):
        allowed_field = 'transaction_status'
        if set(request.data.keys()) != {allowed_field}:
            raise ValidationError(
                f"Only the '{allowed_field}' field can be updated.")

        try:
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=200)
        except Transaction.DoesNotExist:
            return Response("Transaction Id does not exists", status=404)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

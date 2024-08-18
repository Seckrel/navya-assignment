from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import get_template
from core.models import Transaction
from xhtml2pdf.pisa import CreatePDF
from django.http import HttpResponse


class ListTransactionPdf(APIView):
    """
    Generate PDF for Transaction Model

    Args:
        APIView (file): PDF with transaction detail
    """
    allowed_methods = ['get']

    def get(self, request):
        template = get_template('core/pdf/all_transaction_list.html')
        transaction_list = Transaction.objects.all()
        pdf_html = template.render({
            'transactions': transaction_list
        })

        response = HttpResponse(content_type='application/pdf')
        pdf_status = CreatePDF(pdf_html, dest=response)

        if pdf_status.err:
            return Response('Error in generating PDF. Try again', status=400)
        
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response

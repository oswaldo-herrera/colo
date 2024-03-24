from io import BytesIO # nos ayuda a convertir un html en pdf
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from mifiel import Document, Client

def render_to_pdf(template_src, context_dict={},output_path='generated_pdf.pdf'):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        with open(output_path,'wb') as output_file:
            output_file.write(result.getvalue())
            return True
        return False
    return None



def crearMifiel(signatories,file ):
    client = Client(app_id='APP_ID', secret_key='APP_SECRET')
    doc = Document.create(client, signatories, file)

     
    return doc
        
        

import usaddress
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError


class Home(TemplateView):
    template_name = 'parserator_web/index.html'


class AddressParse(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        '''
        Getting data resulting from results of processing requests 
        '''
        address = request.query_params.get('address');

        try:
            # Parse the address
            address_components, address_type = self.parse(address);

            # Return response
            response = {
                'inputString': address,
                'components': address_components,
                'type': address_type
            }
        except Exception as error:
            # Return error
            response = {
                'error': True,
                'exceptionName': type(error).__name__,
                'detail': 'Cannot parse :('
            }
        return Response({response})

    def parse(self, address):
        ''' 
        Parses address using usaddress library
        '''
        address_components, address_type = usaddress.tag(address)
        return address_components, address_type

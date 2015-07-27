from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from devices.authentication import ApikeyAuthentication
from devices.models import Device
from models import DeviceCapture

class DeviceCaptureUploadView(APIView):
    authentication_classes = (ApikeyAuthentication,)

    def post(self, request, *args, **kwargs):
        #get the device that sent the request
        device = Device.objects.get(apikey=request.META.get('HTTP_API_KEY',None))

        longitude = request.query_params.get('longitude',device.longitude)
        latitude = request.query_params.get('latitude',device.latitude)

        if hasattr(request.FILES,"file"):
            file = ContentFile(request.FILES['file'].read())
        else:
            file = ContentFile(request.body)

        deviceCapture = DeviceCapture.objects.create(device=device, longitude=longitude, latitude=latitude, file=file)
        deviceCapture.tags.add(*device.tags.all())
        deviceCapture.save()

        return Response('DeviceCapture result saved')




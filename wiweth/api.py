from rest_framework import views, permissions, response
import datetime
from wiweth.helpers import MapQuestApi, DarkSkyApi


class WeatherView(views.APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        start = request.GET.get('start', '20200101')
        end = request.GET.get('end', '20200131')
        location = request.GET.get('location', 'Cape Town')
        try:
            start_date = datetime.datetime.strptime(start, "%Y%m%d").date()
            end_date = datetime.datetime.strptime(end, "%Y%m%d").date()
            lat , lon = MapQuestApi().location_to_lat_long(location)
            weath = DarkSkyApi(lat, lon)
            print(repr(weath))
            result = weath.get_period_data(start_date, end_date)
            print(repr(result))
        except Exception as e:
            raise e
            return response.Response(repr(e), status=500)

        return response.Response(result)

import logging

from .models import Animal, Species

logger = logging.getLogger('voting_app')


from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.utils import timezone
from datetime import timedelta
import json


class AnimalPopulationView(View):

    def get(self, request):
        queryset = Animal.objects.all()
        return HttpResponse(queryset.count())


class AnimalView(View):

    def get(self, request):
        try:
            print(request.GET)
            name = request.GET.get('name', None)
            if name:
                queryset = Animal.objects.filter(name=name)
            else:
                queryset = Animal.objects.all()
            if queryset:
                data = []
                for query in queryset:
                    new_data = {
                        'name': query.name,
                        'species': query.species.name,
                        'last_feed_time': query.last_feed_time
                    }
                    data.append(new_data)
                return JsonResponse(data, safe=False)
            return JsonResponse([], safe=False, status=404)
        except Exception as e:
            logger.error(str(e))
            return JsonResponse([], safe=False, status=404)

    def post(self, request):
        data = json.loads(request.body)

        name = data.get('name', None)
        species = data.get('species', None)
        print(name, species)
        if len(name) > 30 or len(species) > 30:
            return JsonResponse({"message": "Name or species length must be less than or equal to 30"}, status=422, safe=False)
        queryset = Animal.objects.filter(name=name)
        if queryset:
            # raise forms.ValidationError("Name must be unique")
            return JsonResponse({"message": "Name must be unique"}, status=422, safe=False)
        queryset_species = Species.objects.filter(name=species)
        print(queryset_species)
        if not queryset_species:
            queryset_species = Species.objects.create(name=species)
            print(queryset_species)
        else:
            queryset_species = queryset_species.first()
            print(queryset_species.name)
        Animal.objects.create(name=name, species=queryset_species)
        return JsonResponse(data, status=201, safe=False)


class HungryAnimalsView(View):

    def get(self, request):
        now = timezone.now()
        previous_two_days = now - timedelta(days=2)
        queryset = Animal.objects.filter(last_feed_time__lte=previous_two_days)
        return HttpResponse(queryset.count())


class FeedAnimalView(View):

    def post(self, request):
        name = request.POST.get('name')
        queryset = Animal.objects.filter(name=name)
        if queryset:
            queryset.update(last_feed_time=timezone.now())
        return HttpResponse()

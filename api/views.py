from django.http import JsonResponse

# Create your views here.


def home(request):
    return JsonResponse({'info': 'iPadel Tennis', 'name': 'iPadel Tennis'})

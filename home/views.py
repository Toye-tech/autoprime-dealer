from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Car
from django.views.decorators.cache import never_cache

# ---- PUBLIC STOREFRONT ----
def home(request):
    cars = Car.objects.filter(status='available')
    context = {
        'cars': cars,
        'total_stock': Car.objects.filter(status='available').count(),
        'sold_count': Car.objects.filter(status='sold').count(),
        'min_price': Car.objects.filter(status='available').order_by('price').first(),
    }
    return render(request, 'home/home.html', context)


# ---- CRUD API (protected — staff only) ----

@staff_member_required
def api_cars_list(request):
    """GET all cars for admin dashboard"""
    cars = Car.objects.all().values(
        'id','brand','model','year','category','fuel','transmission',
        'mileage','colour','price','price_note','badge','featured',
        'status','image_url','wa_message'
    )
    return JsonResponse({'cars': list(cars)})


@staff_member_required
@require_POST
def api_car_create(request):
    """POST — create a new car"""
    try:
        data = json.loads(request.body)
        car = Car.objects.create(
            brand        = data.get('brand',''),
            model        = data.get('model',''),
            year         = int(data.get('year', 2024)),
            category     = data.get('category','suv'),
            fuel         = data.get('fuel','Petrol'),
            transmission = data.get('transmission','Automatic'),
            mileage      = int(data.get('mileage', 0)),
            colour       = data.get('colour',''),
            price        = int(data.get('price', 0)),
            price_note   = data.get('priceNote',''),
            badge        = data.get('badge',''),
            featured     = bool(data.get('featured', False)),
            status       = 'available',
            image_url    = data.get('img',''),
            wa_message   = data.get('waMsg',''),
        )
        return JsonResponse({'success': True, 'id': car.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@staff_member_required
@require_http_methods(['PUT'])
def api_car_update(request, car_id):
    """PUT — update an existing car"""
    try:
        car  = get_object_or_404(Car, id=car_id)
        data = json.loads(request.body)
        car.brand        = data.get('brand', car.brand)
        car.model        = data.get('model', car.model)
        car.year         = int(data.get('year', car.year))
        car.category     = data.get('category', car.category)
        car.fuel         = data.get('fuel', car.fuel)
        car.transmission = data.get('transmission', car.transmission)
        car.mileage      = int(data.get('mileage', car.mileage))
        car.colour       = data.get('colour', car.colour)
        car.price        = int(data.get('price', car.price))
        car.price_note   = data.get('priceNote', car.price_note)
        car.badge        = data.get('badge', car.badge)
        car.featured     = bool(data.get('featured', car.featured))
        car.image_url    = data.get('img', car.image_url)
        car.wa_message   = data.get('waMsg', car.wa_message)
        car.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@staff_member_required
@require_http_methods(['DELETE'])
def api_car_delete(request, car_id):
    """DELETE — remove a car"""
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    return JsonResponse({'success': True})


@staff_member_required
@require_POST
def api_car_toggle(request, car_id):
    """POST — toggle available/sold"""
    car = get_object_or_404(Car, id=car_id)
    car.status = 'sold' if car.status == 'available' else 'available'
    car.save()
    return JsonResponse({'success': True, 'status': car.status})
import json, re

from django.http import JsonResponse
from django.views import View

from users.utils import login_required
from .models import Review

class ReviewView(View):
    @login_required
    def post(self,request):
        try:
            data    = json.loads(request.body)
            product_id = data['product_id']
            rating  = data['rating']
            content = data['content']

            if not re.match('^[0-5]+(?=[.]?[0,5]$)', str(rating)):
                return JsonResponse({"message": "Rating_Validation_Error"}, status=400)
            
            Review.objects.create(
                user_id    = request.user.id,
                product_id = product_id,
                rating     = rating,
                content    = content
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "Key_Error"}, status=400)
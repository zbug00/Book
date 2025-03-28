from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
import json
from book.models import Quote
from .models import Quote, Category, Tag

def quote_to_dict(quote):
    return {
        "id": quote.id,
        "text": quote.text,
        "author": quote.author,
        "category": {
            "id": quote.category.id if quote.category else None,
            "name": quote.category.name if quote.category else None
        },
        "tags": [{"id": tag.id, "name": tag.name} for tag in quote.tags.all()],
        "created_at": quote.created_at.isoformat()
    }

def serialize_quote_to_json(quote):
    quote_dict = quote_to_dict(quote)
    return json.dumps(quote_dict, cls=DjangoJSONEncoder)

def get_quote(request, pk):
    try:
        quote = Quote.objects.get(pk=pk)
        json_data = serialize_quote_to_json(quote)
        return JsonResponse(json.loads(json_data), safe=False)
    except Quote.DoesNotExist:
        return JsonResponse({"error": "Quote not found"}, status=404)

@csrf_exempt
def create_quote(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            text = data.get('text')
            author = data.get('author')

            if not text or not author:
                return JsonResponse({"error": "Text and author are required fields."}, status=400)

            category_id = data.get('category', {}).get('id')
            category = None
            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    return JsonResponse({"error": f"Category with id {category_id} does not exist."}, status=400)

            quote = Quote.objects.create(
                text=text,
                author=author,
                category=category
            )
            tags = Tag.objects.filter(id__in=data.get("tags"))
            quote.tags.set(tags)
            return JsonResponse({
                "id": quote.id,
                "text": quote.text,
                "author": quote.author,
                "category": {
                    "id": quote.category.id if quote.category else None,
                    "name": quote.category.name if quote.category else None
                },
                "tags": [{"id": tag.id, "name": tag.name} for tag in quote.tags.all()],
                "created_at": quote.created_at.isoformat()
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Only POST method is allowed."}, status=405)
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

def list_categories(request):
    categories = Category.objects.all()
    data = [{"id": cat.id, "name": cat.name} for cat in categories]
    return JsonResponse(data, safe=False)

def list_tags(request):
    tags = Tag.objects.all()
    data = [{"id": tag.id, "name": tag.name} for tag in tags]
    return JsonResponse(data, safe=False)

@csrf_exempt
def get_quote(request, pk):
    try:
        quote = Quote.objects.get(pk=pk)
    except Quote.DoesNotExist:
        return JsonResponse({"error": "Quote not found"}, status=404)

    if request.method == 'GET':
        # Получить одну цитату
        return JsonResponse(quote_to_dict(quote), safe=False)

    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = json.loads(request.body)

            # Обновляем поля
            if 'text' in data:
                quote.text = data['text']
            if 'author' in data:
                quote.author = data['author']

            # Категория
            if 'category' in data and data['category']:
                category_id = data['category'].get('id')
                if category_id:
                    try:
                        category = Category.objects.get(id=category_id)
                        quote.category = category
                    except Category.DoesNotExist:
                        return JsonResponse({"error": f"Category with id {category_id} does not exist."}, status=400)
                else:
                    quote.category = None
            else:
                quote.category = None

            # Теги
            if 'tags' in data:
                tag_ids = [t.get('id') for t in data['tags'] if t.get('id')]
                tags = Tag.objects.filter(id__in=tag_ids)
                quote.tags.set(tags)

            quote.save()

            return JsonResponse(quote_to_dict(quote), status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'DELETE':
        # Удалить цитату
        quote.delete()
        return JsonResponse({"message": "Quote deleted successfully"}, status=204)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def list_quotes(request):
    quotes = Quote.objects.all()
    data = [quote_to_dict(quote) for quote in quotes]
    return JsonResponse(data, safe=False)

def get_all_data(request):
    categories = list(Category.objects.values("id", "name"))
    tags = list(Tag.objects.values("id", "name"))
    quotes = [
        {
            "id": q.id,
            "text": q.text,
            "author": q.author,
            "category": {
                "id": q.category.id if q.category else None,
                "name": q.category.name if q.category else None
            },
            "tags": [{"id": tag.id, "name": tag.name} for tag in q.tags.all()],
            "created_at": q.created_at.isoformat()
        }
        for q in Quote.objects.all()
    ]

    return JsonResponse({
        "categories": categories,
        "tags": tags,
        "quotes": quotes
    }, safe=False)

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

            tags = Tag.objects.filter(id__in=data.get("tags", []))
            quote.tags.set(tags)

            return JsonResponse(quote_to_dict(quote), status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method is allowed."}, status=405)
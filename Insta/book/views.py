from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from book.models import Quote

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
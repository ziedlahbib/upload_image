import base64
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Document
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        title = request.POST.get('title')  # Get the title from the POST data
        file = request.FILES.get('file')  # Get the uploaded file from the request

        if title and file:
            file_data = file.read()  # Read the file data as binary

            # Save the file data to the database
            document = Document(title=title, file_data=file_data)
            document.save()

            response_data = {
                'status': 'success',
                'message': 'File uploaded successfully',
                'file_id': document.id
            }
            return JsonResponse(response_data)
        else:
            response_data = {
                'status': 'error',
                'message': 'Missing title or file'
            }
            return JsonResponse(response_data, status=400)

    response_data = {
        'status': 'error',
        'message': 'Invalid request method'
    }
    return JsonResponse(response_data, status=405)

def download_file(request, file_id):
    try:
        document = Document.objects.get(id=file_id)
        
        # Convert binary data to base64
        file_data_base64 = base64.b64encode(document.file_data).decode('utf-8')
        
        response_data = {
            'status': 'success',
            'file_name': document.title,
            'file_data': file_data_base64,
            'content_type': 'application/octet-stream'
        }
        return JsonResponse(response_data)
    
    except Document.DoesNotExist:
        response_data = {
            'status': 'error',
            'message': 'File not found'
        }
        return JsonResponse(response_data, status=404)

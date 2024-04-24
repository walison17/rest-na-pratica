import json
from uuid import uuid4
from pathlib import Path
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from devpro.uploads.models import Upload
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from devpro.uploads.r2 import create_presigned_url, get_presigned_url


@csrf_exempt
def create_upload(request):
    body = json.loads(request.body)

    name = body["name"]
    content_type = body["content_type"]
    ext = Path(name).suffix
    key = f"{uuid4()}{ext}"

    presigned_url = create_presigned_url(
        settings.R2_BUCKET,
        object_key=key,
        content_type=content_type,
        expiration=10 * 60,
    )
    Upload.objects.create(
        name=name,
        key=key,
        content_type=content_type,
    )

    return HttpResponse(presigned_url)


def get_upload(request, upload_id):
    upload = get_object_or_404(Upload, pk=upload_id)
    url = get_presigned_url(settings.R2_BUCKET, object_key=upload.key)
    return redirect(url)


# blobs .name .type
# request backend /uploads name="" content_type="" -> url
# axios.put(url, file, {"Content-Type": type})
# onUploadProgress

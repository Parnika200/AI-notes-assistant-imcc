from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import StudyMaterialForm
from .models import StudyMaterial
import logging
from django.contrib import messages

from .forms import StudyMaterialForm
from .models import StudyMaterial
from .text_extraction import (
    NoTextExtractedError,
    extract_text_from_material,
)

logger = logging.getLogger(__name__)
# Content type for each supported file extension
CONTENT_TYPES = {
    "pdf": "application/pdf",
    "txt": "text/plain; charset=utf-8",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def home(request):
    return render(request, "core/home.html")


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


# UPLOAD PDF 
@login_required
def material_list(request):
    materials = StudyMaterial.objects.filter(user=request.user).order_by("-uploaded_at")
 #show all material list
    return render(
        request,
        "core/material_list.html",
        {"materials": materials},
    )

@login_required
def material_upload(request):
    if request.method == "POST":
        form = StudyMaterialForm(request.POST, request.FILES)

        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user
            material.file_type = (
                material.file_path.name.rsplit(".", 1)[-1].upper()
            )
            material.status = "pending"
            material.save()

            try:
                material.extracted_text = extract_text_from_material(material)
                material.status = "processed"
                material.save(update_fields=["extracted_text", "status"])

                messages.success(request, "File uploaded and text extracted.")

            except NoTextExtractedError as error:
                material.status = "failed"
                material.save(update_fields=["status"])
                messages.warning(request, str(error))

            except Exception:
                logger.exception(
                    "Text extraction failed for study material ID %s",
                    material.id,
                )
                material.status = "failed"
                material.save(update_fields=["status"])
                messages.error(
                    request,
                    "The file was uploaded, but its text could not be extracted.",
                )

            return redirect("material_list")

    else:
        form = StudyMaterialForm()

    return render(
        request,
        "core/material_upload.html",
        {"form": form},
    )

@login_required
def material_open(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)

    if material.user_id != request.user.id: #if user not authenticated
        raise PermissionDenied

    try:
        file = material.file_path.open("rb")
    except (FileNotFoundError, ValueError):
        raise Http404("The file could not be found.")

    extension = material.file_path.name.rsplit(".", 1)[-1].lower()

    return FileResponse(
        file,
        content_type=CONTENT_TYPES.get(extension, "application/octet-stream"),
        as_attachment=(extension == "docx"),  # browsers can't display Word files, so download them
        filename=material.file_path.name.rsplit("/", 1)[-1],
    )


@login_required
@require_POST
def material_delete(request, material_id):
    material = get_object_or_404(
        StudyMaterial,
        id=material_id,
        user=request.user,
    )

    # Delete the stored PDF and database record.
    material.file_path.delete(save=False)
    material.delete()

    return redirect("material_list")
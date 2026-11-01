from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import StudyMaterialForm
from .models import StudyMaterial

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
            material.file_type = "PDF"
            material.status = "uploaded"
            material.save()
            return redirect("material_list")
    else:
        form = StudyMaterialForm()#get request

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
        pdf = material.file_path.open("rb")
    except (FileNotFoundError, ValueError):
        raise Http404("The PDF file could not be found.")

    return FileResponse(
        pdf,
        content_type="application/pdf",
        as_attachment=False,
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

    # Delete the stored PDF as well as its database record.
    material.file_path.delete(save=False)
    material.delete()

    return redirect("material_list")
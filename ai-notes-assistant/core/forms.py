from django import forms
from .models import StudyMaterial


# uploading the PDF
class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ["title", "file_path"] #fields of form

    def clean_file_path(self):
        uploaded_file = self.cleaned_data["file_path"]

        if not uploaded_file.name.lower().endswith(".pdf"):
            raise forms.ValidationError("Please upload a PDF file.")

        if uploaded_file.size > 10 * 1024 * 1024: #upto 10mb
            raise forms.ValidationError("The PDF must be 10 MB or smaller.")

        # Check  file content begins like a PDF.
        first_bytes = uploaded_file.read(5)
        uploaded_file.seek(0)

        if first_bytes != b"%PDF-": #check if file is valid(every pdf starts with %PDF)
            raise forms.ValidationError("This file does not appear to be a valid PDF.")

        return uploaded_file
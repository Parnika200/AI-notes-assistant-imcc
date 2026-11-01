from django import forms
from .models import StudyMaterial


# uploading the PDF
import zipfile
from django import forms
from .models import StudyMaterial


class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ["title", "file_path"]  # fields of form

    def clean_file_path(self):
        uploaded_file = self.cleaned_data["file_path"]
        extension = uploaded_file.name.rsplit(".", 1)[-1].lower()

        allowed_extensions = {"pdf", "docx", "txt"}

        if extension not in allowed_extensions:
            raise forms.ValidationError("Upload a PDF, DOCX, or TXT file.")

        if uploaded_file.size > 50 * 1024 * 1024:  # 50 MB
            raise forms.ValidationError("The file must be 50 MB or smaller.")

        if extension == "pdf":
            first_bytes = uploaded_file.read(5)
            uploaded_file.seek(0)

            if first_bytes != b"%PDF-":
                raise forms.ValidationError("This file does not appear to be a valid PDF.")

        elif extension == "docx":
            # A real .docx is a ZIP archive that contains word/document.xml
            try:
                with zipfile.ZipFile(uploaded_file) as z:
                    is_valid = "word/document.xml" in z.namelist()
            except zipfile.BadZipFile:
                is_valid = False
            finally:
                uploaded_file.seek(0)

            if not is_valid:
                raise forms.ValidationError("This file does not appear to be a valid Word document.")

        elif extension == "txt":
            sample = uploaded_file.read(4096)
            uploaded_file.seek(0)

            if b"\x00" in sample:  # null bytes mean it's a binary file
                raise forms.ValidationError("This file does not appear to be a valid text file.")

        return uploaded_file
from django import forms

class UploadFileForm(forms.Form):
    ocr_image = forms.FileField(label='파일 업로드')

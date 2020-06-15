from django.contrib import admin

from .models import Matrix, ChipSeq, MatrixData, ChipData, Publications, TfClass, TranscriptionFactor, UrlTab

# Register your models here.

admin.site.register(Matrix)
admin.site.register(MatrixData)
admin.site.register(ChipSeq)
admin.site.register(ChipData)
admin.site.register(Publications)
admin.site.register(TfClass)
admin.site.register(TranscriptionFactor)
admin.site.register(UrlTab)

from django.contrib import admin

# Register your models here.

from .models import Matrix, ChipSeq, MatrixData, ChipData, Publications, TfClass, TranscriptionFactor, UrlTab

admin.site.register(Matrix)
admin.site.register(MatrixData)
admin.site.register(ChipSeq)
admin.site.register(ChipData)
admin.site.register(Publications)
admin.site.register(TfClass)
admin.site.register(TranscriptionFactor)
admin.site.register(UrlTab)

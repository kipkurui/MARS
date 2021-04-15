from django.contrib import admin

from .models import Motif, ChipSeq, MatrixData, ChipData, TfClass, TranscriptionFactor

# Register your models here.

admin.site.register(Motif)
admin.site.register(MatrixData)
admin.site.register(ChipSeq)
admin.site.register(ChipData)
#admin.site.register(Publications)
admin.site.register(TfClass)
admin.site.register(TranscriptionFactor)
#admin.site.register(UrlTab)

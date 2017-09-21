from django.contrib import admin


# Register your models here.
from.models import Master

class MasterAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "firstname","email", "timestamp"]
	list_filter = ["timestamp"]
	search_fields = ["firstname","lastname","country","email"]

	class Meta:
		model = Master


admin.site.register(Master, MasterAdmin)
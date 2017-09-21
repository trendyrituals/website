from django.contrib import admin

# Register your models here.
from .models import Course, Coin

class CourseAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","file","user_name","subject","timestamp"]
	list_filter = ["timestamp","subject"]
	search_fields = ["course_name", "user_name","subject","id"]
	class Meta:
		model = Course


class CoinAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","coin"]
	list_filter = ["coin"]
	search_fields = ["user_name"]
	class Meta:
		model = Coin






admin.site.register(Course, CourseAdmin)
admin.site.register(Coin, CoinAdmin)

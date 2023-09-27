from django.contrib import admin
from .models import Book, Category,Profile,Cart,Cartitems

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title',)
    # list_filter = ('genre',)
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Cartitems)


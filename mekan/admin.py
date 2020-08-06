from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from mekan.models import *


class ImageInline(admin.TabularInline):
    model = Images
    extra = 5


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['category']
    inlines = [ImageInline]
    prepopulated_fields = {'slug': ('title',)}


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'place', 'image_tag']
    readonly_fields = ('image_tag',)


class MPTTCategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    readonly_fields = ('image_tag',)
    list_filter = ['status']
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count', 'image_tag', 'status')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Place,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Place,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Related products (in tree)'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'place', 'user', 'status']
    list_filter = ['status']


admin.site.register(Category, MPTTCategoryAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)

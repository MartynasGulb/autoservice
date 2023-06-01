from django.contrib import admin
from .models import (Service, VehicleModel,
                     Vehicle, Order,
                     OrderLine, OrderComment,
                     Profile)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_model', 'plate', 'vin', 'owner_name']
    list_filter = ['owner_name', 'vehicle_model__make', 'vehicle_model__model']
    search_fields = ['vin', 'plate', 'vehicle_model__make', 'vehicle_model__model']


class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0


class OrderCommentInLine(admin.TabularInline):
    model = OrderComment
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'date', 'client', 'deadline', 'deadline_overdue']
    list_editable = ['client', 'deadline']
    inlines = [OrderLineInLine, OrderCommentInLine]


admin.site.register(Service, ServiceAdmin)
admin.site.register(VehicleModel)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
admin.site.register(Profile)

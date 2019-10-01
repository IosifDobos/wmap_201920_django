from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import County, ElectoralDivision, SmallArea, UserProfile


class CountyAdmin(admin.OSMGeoAdmin):
    list_display = ["countyname", "total2011", "pop_density", "land_area", "computed_area", ]
    search_fields = ["countyname", ]


class ElectoralDivisionAdmin(admin.OSMGeoAdmin):
    list_display = ["edname", "countyname", "total2011", "pop_density", "land_area", "computed_area", ]
    search_fields = ["edname", "countyname", ]


class SmallAreaAdmin(admin.OSMGeoAdmin):
    list_display = ["small_area", "edname", "countyname", "total2011", "pop_density", "computed_area", ]
    search_fields = ["small_area", "edname", "countyname", ]


class ProfileInline(admin.StackedInline):
    model = UserProfile
    readonly_fields = ('last_location', 'last_modified',)
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'owner'


class OwnerAdmin(UserAdmin):
    inlines = (ProfileInline,)
    ordering = ['username', ]
    readonly_fields = ('id', 'last_login', 'date_joined', 'is_superuser')

    list_display = ['username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_staff', 'is_superuser']
    # fieldsets = (
    #     (None, {'fields': ('id', 'username', 'password')}),
    #     ('Personal Info', {'fields': ('first_name', 'last_name')}),
    #     ('Profile Info', {'fields': ('profile_phone_number', 'photo',)}),
    #     ('Account Status', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)}),
    #     ('Dates', {'fields': ('last_login', 'date_joined', 'created', 'modified')}),
    # )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(OwnerAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), OwnerAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(ElectoralDivision, ElectoralDivisionAdmin)
admin.site.register(SmallArea, SmallAreaAdmin)

from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse

from drfpasswordless.authtoken.models import Token, TokenProxy

User = get_user_model()


class TokenChangeList(ChangeList):
    """Map to matching User id"""
    def url_for_result(self, result):
        pk = result.user.pk
        return reverse('admin:%s_%s_change' % (self.opts.app_label,
                                               self.opts.model_name),
                       args=(quote(pk),),
                       current_app=self.model_admin.admin_site.name)


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'device_type', 'created')
    fields = ('user', 'device_id', 'device_type')
    ordering = ('-created',)
    actions = None  # Actions not compatible with mapped IDs.
    readonly_fields = ("user", "device_id", "device_type")
    list_filter = ("device_type",)

    def get_changelist(self, request, **kwargs):
        return TokenChangeList

    def get_object(self, request, object_id, from_field=None):
        """
        Map from User ID to matching Token.
        """
        queryset = self.get_queryset(request)
        field = User._meta.pk
        try:
            object_id = field.to_python(object_id)
            user = User.objects.filter(**{field.name: object_id}).first()
            return queryset.filter(user=user).first()
        except (queryset.model.DoesNotExist, User.DoesNotExist, ValidationError, ValueError):
            return None

    def delete_model(self, request, obj):
        # Map back to actual Token, since delete() uses pk.
        token = Token.objects.get(key=obj.key)
        return super().delete_model(request, token)


admin.site.register(TokenProxy, TokenAdmin)

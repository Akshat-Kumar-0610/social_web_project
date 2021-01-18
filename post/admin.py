from django.contrib import admin
from .models import post,Comment
from django.contrib.auth import get_user_model
from users.models import Profile
from django.http import HttpResponse
import datetime
from import_export.admin import ImportExportModelAdmin
from openpyxl import Workbook
from django.core.exceptions import PermissionDenied
from datetime import datetime, date
from openpyxl.styles import Font
from unidecode import unidecode




User = get_user_model()
admin.site.unregister(User)
User = get_user_model()
def style_output_file(file):
    black_font = Font(color='000000', bold=True)
    for cell in file["1:1"]:
        cell.font = black_font

    for column_cells in file.columns:
        length = 10 
        length += 10
        file.column_dimensions[column_cells[0].column_letter].width = length

    return file

def convert_data_date(value):
    return value.strftime('%d/%m/%Y')

def convert_boolean_field(value):
    if value:
        return 'Yes'
    return 'No'

def export_as_xls(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = modeladmin.model._meta
    field_names = modeladmin.list_display
    file_name = unidecode(opts.verbose_name)
    fields = [field.name for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    blank_line = []
    if 'password' in fields:
        fields.remove('password')
    wb = Workbook()
    ws = wb.active
    ws.append(fields)
    for obj in queryset:
        row = []
        for field in fields:
            if field !='password':
           
                value = getattr(obj, field)
                if isinstance(value, datetime) or isinstance(value, date):
                    value = convert_data_date(value)
                elif isinstance(value, bool):
                    value = convert_boolean_field(value)
                row.append(str(value))
        ws.append(row)

    ws = style_output_file(ws)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'
    wb.save(response)
    return response
export_as_xls.short_description = "Export as excel"

@admin.register(User)
class Admin(admin.ModelAdmin):
    actions = [export_as_xls]


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    actions = [export_as_xls]  




@admin.register(post)
class post(admin.ModelAdmin):
    actions = [export_as_xls] 


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    actions = [export_as_xls] 




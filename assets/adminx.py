import xadmin
from xadmin import views
from .models import *

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "韩都衣舍测试"
    site_footer = "mxshop"
    # menu_style = "accordion"

class HostAdmin(object):
    list_display = ('hostname','ip','type','parent','position','project','owner')
    search_fields = ('hostname', 'ip','serial_number','asset_number','parent','position')
    list_filter = ('type','parent','idle')

class ProjectAdmin(object):
    list_display = ('name','owner')
    search_fields = ('name')

xadmin.site.register(ProjectProfile,ProjectAdmin)
xadmin.site.register(HostProfile, HostAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
from django.contrib import admin
from .models import Axiom, Tree, Rule, TreeRule



def grow(modeladmin, request, queryset):
    """
    Grows a tree
	"""
    for tree in queryset:
    	tree.grow()
	rows_updated = queryset.count()
    if rows_updated == 1:
        count_bit = "1 tree was"
    else:
        count_bit = "%s trees were" % rows_updated
    modeladmin.message_user(request, "%s successfully grown." % count_bit)


class TreeRuleInline(admin.StackedInline):

    model = TreeRule
    fieldsets = (
        (None,
            { 'fields': (
                "rule",
                "order",
                )
            }
        ),
    )

class TreeAdmin(admin.ModelAdmin):
	actions = [grow,]
	inlines = (TreeRuleInline,)
	model = Tree

admin.site.register(Axiom)
admin.site.register(Tree, TreeAdmin)
admin.site.register(Rule)

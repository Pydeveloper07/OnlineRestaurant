from django.contrib import admin
from .models import Table, ReservedTable, OrderHistory, ProcessingOrder, UserReviews, UserBonus, Bonus

admin.site.register(Table)
admin.site.register(ReservedTable)
admin.site.register(OrderHistory)
admin.site.register(ProcessingOrder)
admin.site.register(Bonus)
admin.site.register(UserBonus)
admin.site.register(UserReviews)

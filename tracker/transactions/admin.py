from admin_auto_filters.filters import AutocompleteFilter
from django.db import connection
from django.contrib import admin
from .models import Exchange, OrderType, Transaction, TransactionSummary
from .sql import BUY_TRANSACTIONS_SUMM_QUERY, SELL_TRANSACTIONS_SUMM_QUERY


@admin.register(OrderType)
class OrderTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    pass


class PairFilter(AutocompleteFilter):
    """
        Pair filter searches for base and quote names
    """
    title = 'Pair'
    field_name = 'pair'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
        Admin panel for transactions
    """
    list_display = ('id', 'user', 'pair', 'order_type',
                    'amount', 'price', 'fee', 'exchange', 'ts')
    list_filter = ['user', PairFilter, 'ts']

    autocomplete_fields = ['pair']

    def get_changeform_initial_data(self, request):
        return {'user': request.user}


@admin.register(TransactionSummary)
class TransactionSummaryAdmin(admin.ModelAdmin):
    """
        Admin panel for transaction summary
    """
    change_list_template = 'admin/transaction_summary_change_list.html'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        response.context_data['buy_transactions_summary'] = []
        response.context_data['sell_transactions_summary'] = []
        response.context_data['profit_transactions_summary'] = []
        with connection.cursor() as cursor:
            cursor.execute(BUY_TRANSACTIONS_SUMM_QUERY.format(
                user_id=request.user.id))
            for row in cursor.fetchall():
                response.context_data['buy_transactions_summary'].append(
                    {'asset': row[0], 'avg_buy_price': row[1],
                        'total_spending': row[2], 'total_invested': row[3],
                        'total_fees': row[4]})

            cursor.execute(SELL_TRANSACTIONS_SUMM_QUERY.format(
                user_id=request.user.id))
            for row in cursor.fetchall():
                response.context_data['sell_transactions_summary'].append(
                    {'asset': row[0], 'avg_sell_price': row[1], 'total_received': row[2],
                     'total_fees': row[3], 'total_amount': row[4],
                     'total_sold': row[5]})

            cursor.execute(SELL_TRANSACTIONS_SUMM_QUERY.format(
                user_id=request.user.id))
            for row in cursor.fetchall():
                response.context_data['profit_transactions_summary'].append(
                    {'asset': row[0], })
            return response

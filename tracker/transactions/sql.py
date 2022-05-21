"""
    Raw SQL queries for the transactions module.
"""

BUY_TRANSACTIONS_SUMM_QUERY = """
            SELECT base.name, 
                AVG(tra.price) AS avg_price,
                SUM((tra.price*tra.amount) + tra.fee) AS total_speding,
                SUM((tra.price*tra.amount)) AS total_invested,
                SUM(tra.fee) AS total_fees
            FROM (
                SELECT * FROM transactions_transaction 
                JOIN transactions_ordertype 
                ON transactions_ordertype.id = transactions_transaction.order_type_id
                WHERE user_id = {user_id} and transactions_ordertype.name like '%Buy%'
            ) as tra
            JOIN assets_pair as pair ON tra.pair_id = pair.id
            LEFT JOIN assets_asset as base ON pair.base_id = base.id
            GROUP BY base.name;
            """

SELL_TRANSACTIONS_SUMM_QUERY = """
            SELECT quote.name, 
                AVG(sells.price) AS avg_price,
                SUM((sells.price*sells.amount) - sells.fee) AS total_received,
                SUM(sells.fee) AS total_fees,
                SUM(sells.amount) AS total_amount,
                SUM(sells.amount*sells.price) AS total_sold           
            FROM (
                SELECT * FROM transactions_transaction 
                JOIN transactions_ordertype 
                ON transactions_ordertype.id = transactions_transaction.order_type_id
                WHERE user_id = {user_id} and transactions_ordertype.name like '%Sell%'
            ) as sells
            JOIN assets_pair as pair ON sells.pair_id = pair.id
            LEFT JOIN assets_asset as quote ON pair.quote_id = quote.id
            GROUP BY quote.name;
            """

PROFIT_TRANSACTIONS_SUMM_QUERY = """
            SELECT buys.name, avg_buy_price, total_buy_amount, total_buy_fees,
                    avg_sell_price, total_sell_amount, total_sell_fees, (avg_sell_price - avg_buy_price) * total_sell_amount AS sell_profit
                FROM (
                    SELECT base.name, 
                        AVG(tra.price) AS avg_buy_price,
                        SUM(tra.amount) AS total_buy_amount,
                        SUM(tra.fee) AS total_buy_fees
                    FROM (
                        SELECT * FROM transactions_transaction 
                        JOIN transactions_ordertype 
                        ON transactions_ordertype.id = transactions_transaction.order_type_id
                        WHERE user_id = 1 and transactions_ordertype.name like '%Buy%'
                    ) as tra
                    JOIN assets_pair as pair ON tra.pair_id = pair.id
                    LEFT JOIN assets_asset as base ON pair.base_id = base.id
                    GROUP BY base.name
                ) as buys

                JOIN (
                    SELECT quote.name, 
                        AVG(sells.price) AS avg_sell_price,
                        SUM(sells.amount) AS total_sell_amount,
                        SUM(sells.fee) AS total_sell_fees
                    FROM (
                        SELECT * FROM transactions_transaction 
                        JOIN transactions_ordertype 
                        ON transactions_ordertype.id = transactions_transaction.order_type_id
                        WHERE user_id = 1 and transactions_ordertype.name like '%Sell%'
                    ) as sells
                    JOIN assets_pair as pair ON sells.pair_id = pair.id
                    LEFT JOIN assets_asset as quote ON pair.quote_id = quote.id
                    GROUP BY quote.name
                ) as sells
                ON buys.name = sells.name
                GROUP BY buys.name;
            """

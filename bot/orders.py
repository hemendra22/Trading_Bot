import logging


def place_order(client, symbol, side, order_type, quantity, price=None):

    try:
        params = {
            "symbol": symbol.upper(),
            "side": side,
            "type": order_type,
            "quantity": quantity
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        logging.info(f"Order Request: {params}")

        response = client.futures_create_order(**params)

        logging.info(f"Order Response: {response}")

        return response

    except Exception as e:
        logging.error(f"Order Failed: {str(e)}")
        raise

import argparse
import sys

from bot.client import get_client
from bot.orders import place_order
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_limit_price
)
from bot.logging_config import setup_logging


def main():

    setup_logging()

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot"
    )

    parser.add_argument("--symbol", required=True, help="Trading pair e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Required for LIMIT orders")

    args = parser.parse_args()

    try:

        side = validate_side(args.side)
        order_type = validate_order_type(args.type)

        validate_limit_price(order_type, args.price)

        client = get_client()

        print("\n========== ORDER REQUEST ==========")
        print(f"Symbol   : {args.symbol}")
        print(f"Side     : {side}")
        print(f"Type     : {order_type}")
        print(f"Quantity : {args.quantity}")

        if order_type == "LIMIT":
            print(f"Price    : {args.price}")

        response = place_order(
            client,
            args.symbol,
            side,
            order_type,
            args.quantity,
            args.price
        )

        print("\n========== ORDER RESPONSE ==========")

        # Check if order was successful
        if isinstance(response, dict) and "orderId" in response and response["orderId"]:
            print("Order ID     :", response["orderId"])
            print("Status       :", response["status"])
            print("Executed Qty :", response["executedQty"])

            avg_price = response.get("avgPrice", "N/A")
            print("Avg Price    :", avg_price)

            print("\n✅ Order placed successfully!")
        else:
            # API returned an error response or empty dict
            if isinstance(response, dict) and "code" in response:
                print("❌ API Error:")
                print("Code         :", response.get("code", "Unknown"))
                print("Message      :", response.get("msg", "Unknown error"))
            else:
                print("❌ Order failed - likely invalid API credentials or network issue")
            sys.exit(1)

    except Exception as e:
        print("\n❌ Error occurred:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()

from flask import Flask, render_template, redirect, request
import os
from dotenv import load_dotenv
import stripe

app = Flask(__name__)

load_dotenv()

PRICE_ID = os.getenv("PRICE_ID")
ENDPOINT_SECRET = os.getenv("ENDPOINT_SECRET")

stripe.api_key = os.getenv("SECRET_KEY")


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://192.168.128.115:5000/"

    # サブスクのセッションを作成する
    checkout_session = stripe.checkout.Session.create(
        success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=domain_url + "cancel",
        payment_method_types=["card"],
        mode="subscription",
        line_items=[
            {
                "price": PRICE_ID,
                "quantity": 1,
            }
        ],
    )
    # 取得したurlにリダイレクト
    return redirect(checkout_session.url)


@app.get("/success")
def success():
    return render_template("success.html")


@app.get("/cancel")
def cancelled():
    return render_template("cancel.html")


@app.post("/webhook")
def webhook():
    # ヘッダー参考
    # https://stripe.com/docs/api/events/types
    signature = request.headers.get("stripe-signature")

    event = stripe.Webhook.construct_event(
        payload=request.data, sig_header=signature, secret=ENDPOINT_SECRET
    )

    # イベントタイプ参考
    # https://stripe.com/docs/api/events/types
    event_type = event["type"]

    print(f"event: {event_type}")

    # サブスク登録に成功した時
    if event_type == "customer.subscription.created":
        print("新規登録に成功しました")
    # サブスクが更新された時
    elif event_type == "customer.subscription.updated":
        print("更新に成功しました。")
    # サブスクがキャンセルされたとき
    elif event_type == "customer.subscription.deleted":
        print("サブスクをキャンセルしました。")
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

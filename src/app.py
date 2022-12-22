from flask import Flask, render_template, redirect
import os
from dotenv import load_dotenv
import stripe

app = Flask(__name__)

load_dotenv()

PRICE_ID = os.getenv('PRICE_ID')
ENDPOINT_SECRET = os.getenv("ENDPOINT_SECRET")

stripe.api_key = os.getenv("SECRET_KEY")

@app.get("/")
def index():
    return render_template("index.html")


@app.get("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://localhost/"
    
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
        ]
    )
    
    return redirect(checkout_session.url)
    


    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
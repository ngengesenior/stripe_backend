from flask import Flask,request
import stripe
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, it worked"

@app.route("/charge",methods=["POST"])
def create_charge():
    post_data = request.get_json()
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    try:
        charge = stripe.Charge.create(
            amount=post_data.get('amount'),
            currency=post_data.get('currency'),
            card=post_data.get('token')
        )
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        generate_exception(e)
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        generate_exception(e)
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed (maybe you changed API keys recently)
        generate_exception(e)
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        generate_exception(e)
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        generate_exception(e)
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        generate_exception(e)

    #Return success response with charge object
    print(charge)
    return jsonify(charge), 200

def generate_exception(error):
    body = error.json_body
    err = body.get('error',{})
    return jsonify(err), error.http_status
    

if __name__ == "__main__":
    app.run()
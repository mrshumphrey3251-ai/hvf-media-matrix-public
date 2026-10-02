"""
=============================================================================
HVF MEDIA MATRIX : STRIPE WEBHOOK LISTENER & PAYMENT TRIGGER
CLASSIFICATION   : PRIVATE_UNREDACTED
VERSION          : 1.0.0
AUTHOR           : JEFFERY HUMPHREY (CEO / FOUNDER)
=============================================================================
DIRECTIVE:
Listen for authenticated Stripe webhook payloads. Intercept successful 
payments, verify the cryptographic signature, and automatically trigger 
the HVF Treasury Routing Engine.
=============================================================================
"""

import os
import sys
import stripe
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Link to the Treasury Engine
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

try:
    from hvf_treasury_router import execute_treasury_routing
except ImportError as e:
    print(f"[FATAL ERROR] Cannot link to Treasury Engine: {e}")
    sys.exit(1)

# Initialize Environment & Security Keys
load_dotenv(override=True)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_placeholder")

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        # Cryptographic Signature Verification
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({"status": "error", "message": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({"status": "error", "message": "Invalid signature"}), 400

    # Execute business logic based on the event type
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Stripe processes in cents; convert to standard USD format
        amount_total_cents = session.get('amount_total', 0)
        gross_revenue_usd = amount_total_cents / 100.0
        
        customer_email = session.get('customer_details', {}).get('email', 'Unknown Client')
        
        print(f"[+] INCOMING PAYMENT INTERCEPTED: ${gross_revenue_usd:,.2f} from {customer_email}")
        
        # Fire the Automated Treasury Routing Engine
        receipt = execute_treasury_routing(gross_revenue_usd, f"Stripe Checkout: {customer_email}")
        print("[+] TREASURY ROUTING EXECUTED SUCCESSFULLY.")
        print(receipt)

    elif event['type'] == 'payment_intent.succeeded':
        # Hook for future direct payment intents
        pass
    else:
        # Unhandled event type
        print(f"[-] Unhandled event type: {event['type']}")

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    print("==================================================")
    print(" HVF PAYMENT TRIGGER : WEBHOOK LISTENER ONLINE")
    print("==================================================")
    print("Listening for Stripe Webhooks on Port 4242...")
    app.run(port=4242)
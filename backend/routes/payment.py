from flask import Blueprint, request, jsonify, current_app, send_file
from utils.jwt_handler import token_required
from utils.pdf_generator import generate_invoice_pdf
from models.payment import create_payment, find_payments_by_user, find_payment_by_invoice
from models.booking import update_booking_status
from models.bus import find_bus_by_id

payment_bp = Blueprint("payment", __name__)


def _new_invoice_id():
    from datetime import datetime

    return "INV" + datetime.utcnow().strftime("%Y%m%d%H%M%S")


@payment_bp.post("/process")
@token_required
def process_payment():
    data = request.get_json(force=True)
    booking_id = data.get("booking_id")
    bus_id = data.get("bus_id")
    payment_method = data.get("payment_method", "UPI")

    if not booking_id or not bus_id:
        return jsonify({"error": "booking_id and bus_id are required"}), 400

    db = current_app.db
    bus = find_bus_by_id(db, bus_id)
    if not bus:
        return jsonify({"error": "Bus not found"}), 404

    amount = bus.get("price", 0)
    invoice_id = _new_invoice_id()
    invoice_path = generate_invoice_pdf(
        invoice_id,
        user_name="User",
        bus_name=bus.get("bus_name"),
        amount=amount,
        output_dir=current_app.config["PDF_STORAGE_PATH"],
    )

    payment = create_payment(
        db,
        request.user_id,
        booking_id,
        amount,
        payment_method,
        status="SUCCESS",
        invoice_pdf_url=invoice_path,
    )
    update_booking_status(db, booking_id, status="SUCCESS", invoice_id=invoice_id)
    return jsonify(payment), 201


@payment_bp.get("/user/<user_id>")
@token_required
def list_user_payments(user_id):
    db = current_app.db
    payments = find_payments_by_user(db, user_id)
    return jsonify(payments)


@payment_bp.get("/invoice/<invoice_id>")
@token_required
def download_invoice(invoice_id):
    db = current_app.db
    payment = find_payment_by_invoice(db, invoice_id)
    if not payment:
        return jsonify({"error": "Invoice not found"}), 404
    return send_file(payment["invoice_pdf_url"], as_attachment=True)

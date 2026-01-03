from models.notification import create_notification


def notify_eta(db, user_id, eta_minutes, bus_name):
    message = f"Your bus {bus_name} will arrive in {eta_minutes} minutes"
    return create_notification(db, user_id, message, eta_minutes=eta_minutes)

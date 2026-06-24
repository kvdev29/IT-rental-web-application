from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

from app.models import db, Asset, User, AuditLog, Rental

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        stats = {
            'total_assets': Asset.query.count(),
            'assets_in_use': Asset.query.filter_by(status='In Use').count(),
            'assets_available': Asset.query.filter_by(status='Available').count(),
            'total_users': User.query.count(),
            'active_users': User.query.filter_by(is_active=True).count(),
            'active_rentals': Rental.query.filter(Rental.status.in_(['Active', 'Overdue'])).count(),
            'overdue_rentals': Rental.query.filter_by(status='Overdue').count(),
        }
        recent_logs = (AuditLog.query
                       .order_by(AuditLog.timestamp.desc())
                       .limit(10).all())
        active_rentals = (Rental.query
                          .filter(Rental.status.in_(['Active', 'Overdue']))
                          .order_by(Rental.return_by)
                          .limit(10).all())
        return render_template('main/dashboard_admin.html',
                               stats=stats,
                               recent_logs=recent_logs,
                               active_rentals=active_rentals)
    else:
        active_rentals = (Rental.query
                          .filter(Rental.user_id == current_user.id,
                                  Rental.status.in_(['Active', 'Overdue']))
                          .order_by(Rental.return_by)
                          .all())
        rental_history = (Rental.query
                          .filter_by(user_id=current_user.id, status='Returned')
                          .order_by(Rental.returned_at.desc())
                          .limit(20)
                          .all())
        stats = {
            'my_active_rentals': len(active_rentals),
            'my_overdue': sum(1 for r in active_rentals if r.status == 'Overdue'),
            'my_total_rentals': Rental.query.filter_by(user_id=current_user.id).count(),
        }
        return render_template('main/dashboard_user.html',
                               stats=stats,
                               active_rentals=active_rentals,
                               rental_history=rental_history)

import json
import bleach
from functools import wraps
from datetime import datetime
from flask import request, abort, current_app
from flask_login import current_user
from app.models import db, AuditLog


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if not current_user.is_admin:
            log_event(
                event_type=AuditLog.EVENT_ACCESS_DENIED,
                description=(
                    f'Non-admin user "{current_user.username}" attempted to '
                    f'access admin-only resource: {request.path}'
                ),
                resource_type='Route',
            )
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


ALLOWED_TAGS = []
ALLOWED_ATTRIBUTES = {}

def sanitize_input(value):
    if value is None:
        return value
    return bleach.clean(str(value), tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRIBUTES, strip=True)


def apply_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    csp_directives = current_app.config.get('CSP_DIRECTIVES', {})
    if csp_directives:
        csp_string = '; '.join(
            f"{key} {value}" for key, value in csp_directives.items()
        )
        response.headers['Content-Security-Policy'] = csp_string
    if not current_app.debug:
        response.headers['Strict-Transport-Security'] = \
            'max-age=31536000; includeSubDomains'
    response.headers['Permissions-Policy'] = \
        'camera=(), microphone=(), geolocation=()'

    return response


def log_event(event_type, description, resource_type=None,
              resource_id=None, user_id=None, extra_data=None):
    if user_id is None:
        try:
            uid = current_user.id if current_user.is_authenticated else None
        except Exception:
            uid = None
    else:
        uid = user_id

    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        ua = request.headers.get('User-Agent', '')[:255]
    except RuntimeError:
        ip = None
        ua = None

    entry = AuditLog(
        user_id=uid,
        event_type=event_type,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        ip_address=ip,
        user_agent=ua,
        extra_data=json.dumps(extra_data) if extra_data else None,
    )

    try:
        db.session.add(entry)
        db.session.commit()
    except Exception as exc:
        # Audit logging must never crash the application
        current_app.logger.error(f'AuditLog write failed: {exc}')
        db.session.rollback()


def log_event_no_commit(event_type, description, resource_type=None,
                         resource_id=None, user_id=None, extra_data=None):
    if user_id is None:
        try:
            uid = current_user.id if current_user.is_authenticated else None
        except Exception:
            uid = None
    else:
        uid = user_id

    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        ua = request.headers.get('User-Agent', '')[:255]
    except RuntimeError:
        ip, ua = None, None

    entry = AuditLog(
        user_id=uid,
        event_type=event_type,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        ip_address=ip,
        user_agent=ua,
        extra_data=json.dumps(extra_data) if extra_data else None,
    )
    db.session.add(entry)

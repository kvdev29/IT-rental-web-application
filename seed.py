from datetime import date, datetime, timedelta
from app import create_app
from app.models import db, User, Asset, Ticket, RentalItem, Rental, AuditLog

app = create_app('development')

with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    admin = User(username='admin', email='admin@lg.local', full_name='Admin', department='IT', role='admin')
    admin.set_password('Admin@12345')

    alice = User(username='alice.jones', email='alice@lg.local', full_name='Alice Jones', department='Finance')
    alice.set_password('Pass@Alice1')

    dave = User(username='dave.brown', email='dave@lg.local', full_name='Dave Brown', department='Marketing', is_active=False)
    dave.set_password('Pass@Dave1')

    db.session.add_all([admin, alice, dave])
    db.session.flush()

    # Asset
    asset = Asset(name='Dell XPS 15', asset_tag='LT-001', asset_type='Laptop',
                  status='In Use', location='London HQ', assigned_to_id=alice.id)
    db.session.add(asset)
    db.session.flush()

    # Ticket
    ticket = Ticket(title='Laptop running slowly',
                    description='My laptop has been very slow since the last Windows update.',
                    priority='High', category='Hardware',
                    raised_by_id=alice.id, related_asset_id=asset.id)
    db.session.add(ticket)

    # Rental catalog
    items = [
        RentalItem(name='Sony WH-1000XM5', category='Headset', location='London', quantity_total=5),
        RentalItem(name='Logitech MX Keys', category='Keyboard', location='London', quantity_total=5),
        RentalItem(name='Logitech MX Master 3S', category='Mouse', location='London', quantity_total=5),
        RentalItem(name='Dell XPS 13', category='Laptop', location='London', quantity_total=3),
        RentalItem(name='Logitech C930e', category='Webcam', location='London', quantity_total=5),
        RentalItem(name='iPhone 15 Pro', category='Phone', location='London', quantity_total=3),
    ]
    db.session.add_all(items)
    db.session.flush()

    # Rentals for alice
    db.session.add_all([
        Rental(item_id=items[0].id, user_id=alice.id,
               return_by=date.today() + timedelta(days=3), status='Active'),
        Rental(item_id=items[2].id, user_id=alice.id,
               return_by=date.today() - timedelta(days=2), status='Overdue'),
        Rental(item_id=items[1].id, user_id=alice.id,
               rented_at=datetime.utcnow() - timedelta(days=10),
               return_by=date.today() - timedelta(days=7),
               returned_at=datetime.utcnow() - timedelta(days=7),
               status='Returned'),
    ])

    # Audit log sample entries
    db.session.add_all([
        AuditLog(user_id=admin.id, event_type=AuditLog.EVENT_LOGIN_SUCCESS,
                 description='Successful login: admin', ip_address='127.0.0.1'),
        AuditLog(user_id=alice.id, event_type=AuditLog.EVENT_LOGIN_SUCCESS,
                 description='Successful login: alice.jones', ip_address='127.0.0.1'),
        AuditLog(user_id=None, event_type=AuditLog.EVENT_LOGIN_FAIL,
                 description='Failed login attempt for username: hacker', ip_address='10.0.0.55'),
    ])

    db.session.commit()
    print('Done. 3 users, 6 rental items, 3 rentals, 1 asset, 1 ticket.')
    print('  admin       / Admin@12345')
    print('  alice.jones / Pass@Alice1')
    print('  dave.brown  / Pass@Dave1  (deactivated)')

# seed.py

from faker import Faker
from app import app, db
from models import Vendor, Sweet, VendorSweet

fake = Faker()

def seed_data():
    with app.app_context():
        try:
            # Delete existing data
            db.session.query(VendorSweet).delete()
            db.session.query(Vendor).delete()
            db.session.query(Sweet).delete()

            # Generate vendors
            for _ in range(10):
                vendor = Vendor(name=fake.company())
                db.session.add(vendor)
                db.session.commit()

            # Generate sweets
            sweets = ['Chocolate', 'Candy', 'Lollipop', 'Gummy bears', 'Marshmallow', 'Jelly beans', 'Licorice',
                      'Caramel', 'Toffee', 'Fudge']
            for sweet in sweets:
                sweet = Sweet(name=sweet)
                db.session.add(sweet)

            db.session.commit()
            print('Vendors seeded.')
            print('Sweets seeded.')

            # Generate vendor_sweets
            vendors = Vendor.query.all()
            sweets = Sweet.query.all()

            for vendor in vendors:
                for _ in range(5):
                    vendor_sweet = VendorSweet(
                        price=fake.random_int(min=1, max=20),
                        vendor_id=vendor.id,
                        sweet_id=fake.random_element(elements=[sweet.id for sweet in sweets])
                    )
                    db.session.add(vendor_sweet)

            db.session.commit()
            print('VendorSweet seeded.')

        except Exception as e:
            print(f"Error: {str(e)}")
            db.session.rollback()
        finally:
            db.session.close()

if __name__ == '__main__':
    seed_data()

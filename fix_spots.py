from app import app
from models.file import db, ParkingLot, ParkingSpot

with app.app_context():
    # Get all parking lots
    lots = ParkingLot.query.all()
    
    for lot in lots:
        # Check how many spots this lot currently has
        existing_spots = ParkingSpot.query.filter_by(lot_id=lot.id).count()
        needed_spots = lot.maximum_number_of_spots - existing_spots
        
        print(f"Lot: {lot.prime_location_name}")
        print(f"  Should have: {lot.maximum_number_of_spots} spots")
        print(f"  Currently has: {existing_spots} spots")
        print(f"  Need to add: {needed_spots} spots")
        
        # Add missing spots
        for i in range(needed_spots):
            spot = ParkingSpot(lot_id=lot.id, status='available')
            db.session.add(spot)
        
        db.session.commit()
        print(f"  ✓ Added {needed_spots} spots")
    
    print("All parking spots have been created!")
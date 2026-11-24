"""Idempotent demo-data loader. Run: python seed.py"""
from app import app
from extensions import db
from models import User, Exchange, Notification
from werkzeug.security import generate_password_hash

DEMO_PASSWORD = "Learvix@123"
USERS = [
 {"name":"Aarav Mehta","email":"demo@learvix.com","avatar":"AM","bio":"Frontend developer who enjoys helping others learn React and JavaScript.","skills_offered":["React","JavaScript","HTML & CSS"],"skills_wanted":["UI/UX Design","Python","Public Speaking"],"rating":4.9,"completed_exchanges":8},
 {"name":"Maya Shah","email":"maya@learvix.com","avatar":"MS","bio":"Product designer focused on accessible interfaces and design systems.","skills_offered":["UI/UX Design","Figma","Wireframing"],"skills_wanted":["React","Photography"],"rating":4.8,"completed_exchanges":12},
 {"name":"Rohan Kulkarni","email":"rohan@learvix.com","avatar":"RK","bio":"Python developer and data enthusiast. Happy to pair-program and explain concepts.","skills_offered":["Python","Data Analysis","SQL"],"skills_wanted":["JavaScript","Cloud Computing"],"rating":4.7,"completed_exchanges":6},
 {"name":"Isha Patil","email":"isha@learvix.com","avatar":"IP","bio":"Communication coach and public speaking enthusiast.","skills_offered":["Public Speaking","Content Writing","Presentation Skills"],"skills_wanted":["Figma","Video Editing"],"rating":5.0,"completed_exchanges":15},
 {"name":"Kabir Desai","email":"kabir@learvix.com","avatar":"KD","bio":"Backend engineer interested in APIs, databases and mentoring beginners.","skills_offered":["Node.js","Database Design","API Development"],"skills_wanted":["React","Python"],"rating":4.6,"completed_exchanges":5},
]
with app.app_context():
    db.create_all()
    records={}
    for item in USERS:
        user=User.query.filter_by(email=item["email"]).first()
        if not user:
            user=User(password=generate_password_hash(DEMO_PASSWORD), **item)
            db.session.add(user)
        else:
            for key,value in item.items(): setattr(user,key,value)
            user.password=generate_password_hash(DEMO_PASSWORD)
        records[item["email"]]=user
    db.session.commit()
    demo=records["demo@learvix.com"]; maya=records["maya@learvix.com"]; rohan=records["rohan@learvix.com"]
    if not Exchange.query.filter_by(user_id=demo.id,partner_id=maya.id).first():
        db.session.add(Exchange(user_id=demo.id,partner_id=maya.id,skill="React",partner_skill="UI/UX Design",status="active",sessions_completed=2,total_sessions=5))
    if not Exchange.query.filter_by(user_id=demo.id,partner_id=rohan.id).first():
        db.session.add(Exchange(user_id=demo.id,partner_id=rohan.id,skill="JavaScript",partner_skill="Python",status="completed",sessions_completed=4,total_sessions=4,rating=5))
    if not Notification.query.filter_by(user_id=demo.id,title="Welcome to Learvix").first():
        db.session.add(Notification(user_id=demo.id,title="Welcome to Learvix",message="Your learning space is ready. Explore partners and start a skill exchange.",type="success"))
    db.session.commit()
    print("Demo data ready.")
    print("Login: demo@learvix.com / Learvix@123")

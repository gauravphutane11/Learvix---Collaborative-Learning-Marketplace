"""Learvix API — secure, demo-friendly Flask application."""
import os, re
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from dotenv import load_dotenv
load_dotenv()
from extensions import db
from models import User, Exchange, Notification, SkillProofAttempt
from skillproof_bank import SKILL_BANK, public_quiz, grade_quiz


def create_app():
    app = Flask(__name__)
    database_url = os.getenv("DATABASE_URL", "sqlite:///learvix.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    if os.getenv("FLASK_ENV") == "production" and not os.getenv("JWT_SECRET_KEY"):
        raise RuntimeError("JWT_SECRET_KEY must be configured in production")
    app.config.update(
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "dev-only-change-this-secret"),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=int(os.getenv("JWT_TOKEN_HOURS", "8"))),
        MAX_CONTENT_LENGTH=1 * 1024 * 1024,
        JSON_SORT_KEYS=False,
    )
    db.init_app(app)
    JWTManager(app)
    origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()]
    CORS(app, resources={r"/api/*": {"origins": origins}}, supports_credentials=False)

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(self), microphone=(self), geolocation=()"
        response.headers["Cache-Control"] = "no-store" if request.path.startswith("/api") else "public, max-age=300"
        return response

    @app.errorhandler(413)
    def too_large(_): return jsonify(msg="Request is too large"), 413

    @app.errorhandler(404)
    def not_found(_): return jsonify(msg="Resource not found"), 404

    @app.errorhandler(500)
    def server_error(_):
        db.session.rollback()
        app.logger.exception("Unhandled server error")
        return jsonify(msg="Something went wrong. Please try again."), 500

    def payload():
        value = request.get_json(silent=True)
        return value if isinstance(value, dict) else {}

    @app.get("/")
    def health(): return jsonify(status="ok", service="Learvix API", version="1.0")

    @app.get("/api/health")
    def api_health(): return jsonify(status="ok")

    @app.post("/api/register")
    def register():
        data = payload(); name = str(data.get("name", "")).strip(); email = str(data.get("email", "")).strip().lower(); password = str(data.get("password", ""))
        if not name or len(name) > 80: return jsonify(msg="Name is required (maximum 80 characters)"), 400
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) or len(email) > 128: return jsonify(msg="Enter a valid email address"), 400
        if len(password) < 8 or len(password) > 128: return jsonify(msg="Password must be 8–128 characters"), 400
        if User.query.filter_by(email=email).first(): return jsonify(msg="An account with this email already exists"), 409
        user = User(name=name, email=email, password=generate_password_hash(password), avatar="🙂", bio="New to Learvix")
        db.session.add(user); db.session.commit()
        token = create_access_token(identity=str(user.id))
        return jsonify(msg="Account created", access_token=token, user=user.to_dict()), 201

    @app.post("/api/login")
    def login():
        data = payload(); email = str(data.get("email", "")).strip().lower(); password = str(data.get("password", ""))
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password): return jsonify(msg="Invalid email or password"), 401
        return jsonify(access_token=create_access_token(identity=str(user.id)), user=user.to_dict())

    @app.get("/api/me")
    @jwt_required()
    def me():
        user = db.session.get(User, int(get_jwt_identity()))
        if not user: return jsonify(msg="Account not found"), 404
        return jsonify(user.to_dict())

    @app.put("/api/me")
    @jwt_required()
    def update_me():
        user = db.session.get(User, int(get_jwt_identity())); data = payload()
        if "name" in data:
            name = str(data["name"]).strip()
            if not name or len(name) > 80: return jsonify(msg="Name must be 1–80 characters"), 400
            user.name = name
        if "bio" in data: user.bio = str(data["bio"])[:500]
        if "avatar" in data: user.avatar = str(data["avatar"])[:10]
        if "profileImage" in data:
            image = data["profileImage"]
            if image is not None and image != "":
                if not isinstance(image, str) or len(image) > 650000 or not re.match(r"^data:image/(png|jpeg|webp);base64,[A-Za-z0-9+/]+={0,2}$", image):
                    return jsonify(msg="Profile photo must be a PNG, JPG or WEBP image smaller than 450 KB"), 400
                user.profile_image = image
            else:
                user.profile_image = None
        for key, field in (("skillsOffered", "skills_offered"), ("skillsWanted", "skills_wanted")):
            if key in data:
                values = data[key]
                if not isinstance(values, list) or len(values) > 30 or any(not isinstance(x, str) or not x.strip() or len(x) > 50 for x in values): return jsonify(msg=f"{key} must be a list of up to 30 valid skills"), 400
                setattr(user, field, list(dict.fromkeys(x.strip() for x in values)))
        db.session.commit(); return jsonify(user.to_dict())

    @app.get("/api/users")
    @jwt_required()
    def users():
        me_id = int(get_jwt_identity())
        return jsonify([{k:v for k,v in u.to_dict().items() if k != "email"} for u in User.query.filter(User.id != me_id).order_by(User.name).all()])

    @app.get("/api/users/<int:user_id>")
    @jwt_required()
    def get_user(user_id):
        u = db.session.get(User, user_id)
        if not u: return jsonify(msg="User not found"), 404
        data = u.to_dict(); data.pop("email", None); data.pop("activeMatches", None)
        return jsonify(data)

    @app.get("/api/matches")
    @jwt_required()
    def matches():
        me = db.session.get(User, int(get_jwt_identity())); wanted=set(me.skills_wanted or []); offered=set(me.skills_offered or []); results=[]
        for u in User.query.filter(User.id != me.id).all():
            learn=sorted(wanted.intersection(u.skills_offered or [])); teach=sorted(offered.intersection(u.skills_wanted or []))
            if learn or teach:
                score=min(100, (len(learn)+len(teach))*25 + (20 if learn and teach else 0))
                results.append({"id":u.id,"name":u.name,"avatar":u.avatar,"profileImage":u.profile_image,"bio":u.bio,"rating":u.rating,"skillsOffered":u.skills_offered or [],"skillsWanted":u.skills_wanted or [],"commonSkills":learn,"skillsTheyWantFromYou":teach,"matchScore":score,"mutualExchange":bool(learn and teach)})
        return jsonify(sorted(results,key=lambda x:(x["matchScore"],x["rating"] or 0),reverse=True))

    @app.get("/api/exchanges")
    @jwt_required()
    def exchanges():
        uid=int(get_jwt_identity()); rows=Exchange.query.filter(or_(Exchange.user_id==uid,Exchange.partner_id==uid)).order_by(Exchange.start_date.desc()).all()
        return jsonify([x.to_dict() for x in rows])

    @app.post("/api/exchanges")
    @jwt_required()
    def create_exchange():
        uid=int(get_jwt_identity()); data=payload(); partner_id=data.get("partner_id")
        try: partner_id=int(partner_id)
        except (TypeError,ValueError): return jsonify(msg="A valid learning partner is required"),400
        partner=db.session.get(User,partner_id)
        skill=str(data.get("skill", "")).strip(); partner_skill=str(data.get("partner_skill", "")).strip()
        if not partner or partner.id==uid: return jsonify(msg="Choose another registered user"),400
        if not skill or not partner_skill or len(skill)>100 or len(partner_skill)>100: return jsonify(msg="Both exchange skills are required"),400
        try: total=max(1,min(30,int(data.get("total_sessions",5))))
        except (TypeError,ValueError): return jsonify(msg="Total sessions must be between 1 and 30"),400
        sender=db.session.get(User,uid); ex=Exchange(user_id=uid,partner_id=partner_id,skill=skill,partner_skill=partner_skill,total_sessions=total,status="pending")
        db.session.add(ex); db.session.flush()
        db.session.add(Notification(user_id=partner_id,title="New learning request",message=f"{sender.name} wants to exchange {skill} for {partner_skill}.",type="info",related_exchange_id=ex.id))
        db.session.commit(); return jsonify(ex.to_dict()),201

    @app.patch("/api/exchanges/<int:exchange_id>")
    @jwt_required()
    def update_exchange(exchange_id):
        uid=int(get_jwt_identity()); ex=db.session.get(Exchange,exchange_id); data=payload()
        if not ex: return jsonify(msg="Exchange not found"),404
        if uid not in (ex.user_id,ex.partner_id): return jsonify(msg="You are not part of this exchange"),403
        if "status" in data:
            status=data["status"]
            if status not in ("pending","active","rejected","completed","cancelled"): return jsonify(msg="Invalid exchange status"),400

            # Only the recipient can accept or reject a pending request.
            if status in ("active","rejected"):
                if uid != ex.partner_id:
                    return jsonify(msg="Only the recipient can accept or reject this request"),403
                if ex.status != "pending":
                    return jsonify(msg="This request has already been answered"),409

            # Pending is the initial state created by POST /api/exchanges.
            if status == "pending":
                return jsonify(msg="A request cannot be reset to pending"),400

            if status == "completed" and ex.status != "active":
                return jsonify(msg="Only an active exchange can be completed"),409

            ex.status=status
        if "sessions_completed" in data:
            try: count=int(data["sessions_completed"])
            except (TypeError,ValueError): return jsonify(msg="Invalid session count"),400
            if count < ex.sessions_completed or count > ex.total_sessions: return jsonify(msg="Session count must be between current progress and total sessions"),400
            if ex.status!="active": return jsonify(msg="Only active exchanges can log sessions"),409
            ex.sessions_completed=count
        if "rating" in data:
            try: rating=int(data["rating"])
            except (TypeError,ValueError): return jsonify(msg="Rating must be between 1 and 5"),400
            if not 1<=rating<=5 or ex.status!="completed": return jsonify(msg="Rate a completed exchange from 1 to 5"),400
            ex.rating=rating
        other=ex.partner_id if uid==ex.user_id else ex.user_id; actor=db.session.get(User,uid)
        if "status" in data or "sessions_completed" in data:
            if ex.status == "active":
                notification_title = "Exchange accepted"
                notification_message = f"{actor.name} accepted exchange #{ex.id}."
            elif ex.status == "rejected":
                notification_title = "Exchange declined"
                notification_message = f"{actor.name} declined exchange #{ex.id}."
            else:
                notification_title = "Exchange updated"
                notification_message = f"{actor.name} updated your exchange #{ex.id}."
            db.session.add(Notification(
                user_id=other,
                title=notification_title,
                message=notification_message,
                type="success" if ex.status in ("active", "completed") else "info",
                related_exchange_id=ex.id
            ))
        db.session.commit(); return jsonify(ex.to_dict())

    @app.get("/api/skillproof/skills")
    @jwt_required()
    def skillproof_skills():
        user = db.session.get(User, int(get_jwt_identity()))
        attempts = SkillProofAttempt.query.filter_by(user_id=user.id).order_by(SkillProofAttempt.created_at.desc()).all()
        best = {}
        for attempt in attempts:
            best[attempt.skill] = max(best.get(attempt.skill, 0), attempt.score)
        return jsonify({"skills": [{"name": name, "questionCount": len(items), "bestScore": best.get(name), "verified": best.get(name, 0) >= 80} for name, items in SKILL_BANK.items()], "verifiedSkills": user.verified_skills or [], "trustedMember": bool(user.verified_skills or [])})

    @app.get("/api/skillproof/quiz/<path:skill>")
    @jwt_required()
    def skillproof_quiz(skill):
        if skill not in SKILL_BANK: return jsonify(msg="Skill assessment not found"), 404
        return jsonify({"skill": skill, "questionCount": len(SKILL_BANK[skill]), "questions": public_quiz(skill)})

    @app.post("/api/skillproof/attempts")
    @jwt_required()
    def skillproof_submit():
        data = payload(); skill = data.get("skill"); answers = data.get("answers")
        if skill not in SKILL_BANK: return jsonify(msg="Choose a supported skill"), 400
        if not isinstance(answers, dict) or len(answers) != len(SKILL_BANK[skill]): return jsonify(msg="Answer all 10 questions before submitting"), 400
        for key, value in answers.items():
            if key not in {str(i) for i in range(1, 11)} or isinstance(value, bool) or not isinstance(value, int) or value not in range(4):
                return jsonify(msg="Invalid answer data"), 400
        correct, details = grade_quiz(skill, answers)
        score = round(correct * 10)
        passed = score >= 80
        user = db.session.get(User, int(get_jwt_identity()))
        attempt = SkillProofAttempt(user_id=user.id, skill=skill, score=score, correct_answers=correct, total_questions=10, passed=passed)
        db.session.add(attempt)
        if passed:
            verified = list(user.verified_skills or [])
            is_new_badge = skill not in verified
            if is_new_badge:
                verified.append(skill)
                user.verified_skills = verified
                db.session.add(Notification(user_id=user.id, title="SkillProof badge earned", message=f"You scored {score}% in {skill} and earned a verified skill badge.", type="success"))
        db.session.commit()
        return jsonify({"attempt": attempt.to_dict(), "details": details, "verifiedSkills": user.verified_skills or [], "trustedMember": bool(user.verified_skills or []), "message": "Skill verified! You earned a SkillProof badge." if passed else "Assessment recorded. Score 80% or higher to verify this skill."})

    @app.get("/api/skillproof/attempts")
    @jwt_required()
    def skillproof_attempts():
        uid = int(get_jwt_identity())
        attempts = SkillProofAttempt.query.filter_by(user_id=uid).order_by(SkillProofAttempt.created_at.desc()).limit(50).all()
        return jsonify([item.to_dict() for item in attempts])

    @app.get("/api/notifications")
    @jwt_required()
    def notifications():
        uid=int(get_jwt_identity()); rows=Notification.query.filter_by(user_id=uid).order_by(Notification.created_at.desc()).limit(100).all()
        return jsonify([n.to_dict() for n in rows])

    @app.patch("/api/notifications/<int:notification_id>/read")
    @jwt_required()
    def read_notification(notification_id):
        uid=int(get_jwt_identity()); n=db.session.get(Notification,notification_id)
        if not n: return jsonify(msg="Notification not found"),404
        if n.user_id!=uid: return jsonify(msg="Not allowed"),403
        n.read=True; db.session.commit(); return jsonify(n.to_dict())

    @app.patch("/api/notifications/read-all")
    @jwt_required()
    def read_all():
        uid=int(get_jwt_identity()); count=Notification.query.filter_by(user_id=uid,read=False).update({"read":True}); db.session.commit()
        return jsonify(msg="Notifications marked as read",count=count)

    with app.app_context():
        db.create_all()
        # Additive compatibility for existing SQLite demo databases.
        if database_url.startswith("sqlite"):
            from sqlalchemy import inspect, text
            columns = {c["name"] for c in inspect(db.engine).get_columns("user")}
            with db.engine.begin() as conn:
                if "profile_image" not in columns: conn.execute(text("ALTER TABLE user ADD COLUMN profile_image TEXT"))
                if "verified_skills" not in columns: conn.execute(text("ALTER TABLE user ADD COLUMN verified_skills JSON"))
    return app

app=create_app()
if __name__ == "__main__": app.run(host="127.0.0.1",port=int(os.getenv("PORT",5000)),debug=os.getenv("FLASK_DEBUG")=="1")

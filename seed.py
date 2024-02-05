import os
from flask import Flask
from db.shared import db
from db.models.user_post import UserPost
from db.models.post import Post
from db.models.user import User

SEED_PASSWORD = "123456"

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DB_PATH", "sqlite:///database.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def reset(db):
    try:
        UserPost.__table__.drop(db.engine)
        User.__table__.drop(db.engine)
        Post.__table__.drop(db.engine)
    except:
        pass
    db.create_all()
    print("db is reset!")

def seed(db):
    try:
        with db.session.begin_nested():
            user1 = User(username="thomas", password=SEED_PASSWORD)
            db.session.add(user1)

            user2 = User(username="santiago", password=SEED_PASSWORD)
            db.session.add(user2)

            user3 = User(username="ashanti", password=SEED_PASSWORD)
            db.session.add(user3)

            user4 = User(username="julia", password=SEED_PASSWORD)
            db.session.add(user4)

            user5 = User(username="cheng", password=SEED_PASSWORD)
            db.session.add(user5)

            post1 = Post(
                text="Excepteur occaecat minim reprehenderit cupidatat dolore voluptate velit labore pariatur culpa esse mollit. Veniam ipsum amet eu dolor reprehenderit quis tempor pariatur labore. Tempor excepteur velit dolor commodo aute. Proident aute cillum dolor sint laborum tempor cillum voluptate minim. Amet qui eiusmod duis est labore cupidatat excepteur occaecat nulla.",
                likes=12,
                reads=5,
                tags=["food", "recipes", "baking"],
                popularity=0.19,
            )
            db.session.add(post1)

            post2 = Post(
                text="Ea cillum incididunt consequat ullamco nisi aute labore cupidatat exercitation et sunt nostrud. Occaecat elit tempor ex anim non nulla sit culpa ipsum aliquip. In amet in Lorem ut enim. Consectetur ea officia reprehenderit pariatur magna eiusmod voluptate. Nostrud labore id adipisicing culpa sunt veniam qui deserunt magna sint mollit. Cillum irure pariatur occaecat amet reprehenderit nisi qui proident aliqua.",
                likes=104,
                reads=200,
                tags=["travel", "hotels"],
                popularity=0.7,
            )
            db.session.add(post2)

            post3 = Post(
                text="Voluptate consequat minim commodo nisi minim ut. Exercitation incididunt eiusmod qui duis enim sunt dolor sit nisi laboris qui enim mollit. Proident pariatur elit est elit consectetur. Velit anim eu culpa adipisicing esse consequat magna. Id do aliquip pariatur laboris consequat cupidatat voluptate incididunt sint ea.",
                likes=10,
                reads=32,
                tags=["travel", "airbnb", "vacation"],
                popularity=0.7,
            )
            db.session.add(post3)

            post4 = Post(
                text="This is post 4",
                likes=50,
                reads=300,
                tags=["vacation", "spa"],
                popularity=0.4,
            )
            db.session.add(post4)

            post5 = Post(
                text="Nulla minim irure duis cillum dolore minim enim officia nulla ut. Tempor magna pariatur velit ea cillum reprehenderit. Commodo laborum ullamco est dolore ea nostrud excepteur cupidatat esse. Esse cupidatat velit aliquip aliquip consectetur duis veniam excepteur anim deserunt. Do irure id aute culpa deserunt aute sit ad irure ullamco enim non cupidatat.",
                likes=13,
                reads=14,
                tags=["tech", "music", "spa"],
                popularity=0.64,
            )
            db.session.add(post5)

            post6 = Post(
                text="Id nulla sunt ipsum consectetur commodo deserunt exercitation nostrud consectetur. Aliquip irure Lorem non aliqua. Anim do eu consectetur adipisicing sunt mollit non.",
                likes=16,
                reads=57,
                tags=["spa", "art", "fashion"],
                popularity=0.68,
            )
            db.session.add(post6)

            post7 = Post(
                text="Ullamco deserunt et eu aliqua est et consequat fugiat sunt adipisicing ipsum. Incididunt fugiat esse amet dolore sunt quis officia minim minim. Esse ullamco duis eu qui enim in nulla enim eu aliquip nisi sunt laboris. Est commodo aliquip dolor nulla anim.",
                likes=11,
                reads=38,
                tags=["vacation", "fashion", "food"],
                popularity=0.2,
            )
            db.session.add(post7)

            post8 = Post(
                text="Ex labore cillum aute in proident nostrud in. Adipisicing tempor Lorem occaecat ea quis ad ex velit sit cillum adipisicing. Adipisicing dolore velit aliqua in sunt duis ad adipisicing. Ut duis sit deserunt mollit velit cillum aute commodo ea nisi. Laboris enim ex cillum tempor amet do proident eu consectetur. Adipisicing elit ipsum et sit sunt esse laborum enim laborum.",
                likes=0,
                reads=17,
                tags=["art", "hotel","beach"],
                popularity=0.06,
            )
            db.session.add(post8)

            post9 = Post(
                text="Quis sint amet ex ea cillum. Cillum eiusmod sit dolor proident. Exercitation enim sunt tempor tempor laborum dolor enim esse irure. Labore ut sit culpa sunt nostrud laboris. Adipisicing proident ea amet duis cillum do quis ipsum nostrud elit occaecat qui veniam. Laborum eu nostrud laboris labore ipsum id non Lorem dolor.",
                likes=0,
                reads=71,
                tags=["art", "spa", "beach"],
                popularity=0.78,
            )
            db.session.add(post9)
        db.session.commit()

        # Assigning posts to users
        db.session.add(UserPost(user_id=user1.id, post_id=post1.id))

        db.session.add(UserPost(user_id=user2.id, post_id=post1.id))
        db.session.add(UserPost(user_id=user2.id, post_id=post2.id))

        db.session.add(UserPost(user_id=user3.id, post_id=post3.id))
        db.session.add(UserPost(user_id=user3.id, post_id=post4.id))
        db.session.add(UserPost(user_id=user3.id, post_id=post5.id))

        db.session.add(UserPost(user_id=user4.id, post_id=post4.id))
        db.session.add(UserPost(user_id=user4.id, post_id=post5.id))
        db.session.add(UserPost(user_id=user4.id, post_id=post6.id))
        db.session.add(UserPost(user_id=user4.id, post_id=post7.id))
        
        db.session.add(UserPost(user_id=user5.id, post_id=post5.id))
        db.session.add(UserPost(user_id=user5.id, post_id=post6.id))
        db.session.add(UserPost(user_id=user5.id, post_id=post7.id))
        db.session.add(UserPost(user_id=user5.id, post_id=post8.id))
        db.session.add(UserPost(user_id=user5.id, post_id=post9.id))
        db.session.commit()
        print("seeded users and posts")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {str(e)}")

if __name__ == "__main__":
    with create_app().app_context():
        db.create_all()
        print("seeding...")
        reset(db)
        seed(db)

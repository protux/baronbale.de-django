import sys, logging

from peewee import PostgresqlDatabase, Model, CharField, DateTimeField, BooleanField, ForeignKeyField, TextField, IntegerField
from baronbale_website import settings

from . import utils

if settings.DEBUG:
    SQLITE_DB_PATH = 'finya.db'
    from peewee import SqliteDatabase
    db = SqliteDatabase(SQLITE_DB_PATH)
else:
    db = PostgresqlDatabase(
        'finya',
        user='finya', 
        password='8Oeol0eEK2n5vk6tVCSI',
        host='127.0.0.1',
    )

class Question(Model):
    question = CharField(max_length=100, unique=True)
    
    class Meta:
        database = db

class BrandCategory(Model):
    name = CharField(max_length=30)
    
    class Meta:
        database = db

class Brand(Model):
    brand_id = IntegerField()
    name = CharField(max_length=50)
    category = ForeignKeyField(
        BrandCategory,
        on_delete='CASCADE'
    )
    
    class Meta:
        database = db

class RelationshipGoal(Model):
    goal = CharField(max_length=50)
    
    class Meta:
        database = db

class Language(Model):
    name = CharField(max_length=20)
    
    class Meta:
        database = db

class FinyaUser(Model):
    name = CharField(max_length=14)
    uid = CharField(max_length=10)
    gender = IntegerField(default=0)
    joined = DateTimeField(default=utils.get_local_time())
    removed = DateTimeField(null=True)
    last_updated = DateTimeField(null=True)
    
    class Meta:
        database = db

        indexes = (
            (('name', 'uid'), True),
        )

class Profile(Model):
    zip_area = CharField(max_length=2, null=True)
    town = CharField(max_length=100)
    relationship_status = CharField(max_length=30, null=True)
    preferred_gender = CharField(max_length=10, null=True)
    preferred_age_from = IntegerField(default=0)
    preferred_age_to = IntegerField(default=1000)
    statement = TextField(null=True)
    picture_rating = IntegerField(null=True)
    height = IntegerField(null=True)
    shape = CharField(max_length=20, null=True)
    eye_color = CharField(max_length=20, null=True)
    hair_color = CharField(max_length=15, null=True)
    haircut = CharField(max_length=20, null=True)
    industry = CharField(max_length=50, null=True)
    job = CharField(max_length=40, null=True)
    last_school = CharField(max_length=25, null=True)
    children = CharField(max_length=25, null=True)
    children_preference = CharField(max_length=20, null=True)
    smoking = CharField(max_length=20, null=True)
    moving_preference = CharField(max_length=30, null=True)
    zodiac = CharField(max_length=15, null=True)
    feeling = CharField(max_length=15, null=True)
    appreciated_activity = CharField(max_length=20, null=True)
    age = IntegerField()
    user = ForeignKeyField(
        FinyaUser,
        on_delete='CASCADE'
    )

    updated = DateTimeField(null=True)
    previous_profile = ForeignKeyField(
        'self', 
        null=True,
        on_delete='CASCADE'
    )
    
    def equals_ignore_id(self, other):
        if isinstance(other, Profile):
            return self.zip_area == other.zip_area and\
                self.town == other.town and\
                self.relationship_status == other.relationship_status and\
                self.preferred_gender == other.preferred_gender and\
                self.preferred_age_from == other.preferred_age_from and\
                self.preferred_age_to == other.preferred_age_to and\
                self.statement == other.statement and\
                self.height == other.height and\
                self.shape == other.shape and\
                self.eye_color == other.eye_color and\
                self.hair_color == other.hair_color and\
                self.haircut == other.haircut and\
                self.industry == other.industry and\
                self.job == other.job and\
                self.last_school == other.last_school and\
                self.children == other.children and\
                self.children_preference == other.children_preference and\
                self.smoking == other.smoking and\
                self.moving_preference == other.moving_preference and\
                self.zodiac == other.zodiac and\
                self.feeling == other.feeling and\
                self.appreciated_activity == other.appreciated_activity and\
                self.age == other.age and\
                self.user == other.user and\
                self.updated == other.updated and\
                self.previous_profile == other.previous_profile
        return False

    class Meta:
        database = db

class GuestbookEntry(Model):
    profile = ForeignKeyField(
        Profile,
        on_delete='CASCADE'
    )
    author_name = CharField(max_length=14)
    author_age = IntegerField()
    date_authored = DateTimeField()
    entry = CharField(max_length=500)
    removed = DateTimeField(null=True)

    class Meta:
        database = db

class ProfileLanguage(Model):
    language = ForeignKeyField(
        Language,
        on_delete='CASCADE'
    )
    profile = ForeignKeyField(
        Profile,
        on_delete='CASCADE'
    )
    added = DateTimeField(default=utils.get_local_time())
    removed = DateTimeField(null=True)
    
    class Meta:
        database = db

class ProfileRelationshipGoal(Model):
    relationship_goal = ForeignKeyField(
        RelationshipGoal,
        on_delete='CASCADE'
    )
    profile = ForeignKeyField(
        Profile,
        on_delete='CASCADE'
    )
    added = DateTimeField(default=utils.get_local_time())
    removed = DateTimeField(null=True)
    
    class Meta:
        database = db

class ProfileBrand(Model):
    brand = ForeignKeyField(
        Brand,
        on_delete='CASCADE'
    )
    profile = ForeignKeyField(
        Profile,
        on_delete='CASCADE'
    ) 
    added = DateTimeField(default=utils.get_local_time())
    removed = DateTimeField(null=True)
    
    class Meta:
        database = db

class ProfileImage(Model):
    name = CharField(max_length=100)
    image = TextField()
    removed = DateTimeField(null=True)
    added = DateTimeField(default=utils.get_local_time())
    profile = ForeignKeyField(
        Profile,
        on_delete='CASCADE'
    )
    
    class Meta:
        database = db

class Answer(Model):
    question = ForeignKeyField(
        Question,
        on_delete='CASCADE'
    )
    answer = CharField(max_length=500)
    removed = DateTimeField(null=True)
    updated = DateTimeField(null=True)
    previous_version = ForeignKeyField(
        'self', 
        null=True,
        on_delete='CASCADE'
    )
    profile = ForeignKeyField(
        Profile,
        on_delete='CASCADE'
    )
    answered = DateTimeField(default=utils.get_local_time())
    
    class Meta:
        database = db

class Preference(Model):
    preference = CharField(max_length=50)
    removed = DateTimeField(null=True)
    added = DateTimeField(default=utils.get_local_time())
    profile = ForeignKeyField(
        Profile,
        on_delete='CASCADE'
    )
    
    class Meta:
        database = db

class Adversion(Model):
    adversion = CharField(max_length=50)
    removed = DateTimeField(null=True)
    added = DateTimeField(default=utils.get_local_time())
    profile = ForeignKeyField(
        Profile,
        on_delete='CASCADE'
    )
    
    class Meta:
        database = db

def init():
    db.connect()
    db.create_tables([Question, BrandCategory, Brand, RelationshipGoal, GuestbookEntry, Language, Profile, ProfileLanguage, ProfileRelationshipGoal, ProfileBrand, ProfileImage, Answer, Preference, Adversion, FinyaUser]) 
    db.close()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        init()

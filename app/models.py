from . import db
from sqlalchemy import union

class PeakAgentProduct(db.Model):
    __tablename__ = 'peak_agent_products'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=True)
    lower_limit = db.Column(db.Integer)
    upper_limit = db.Column(db.Integer)
    price = db.Column(db.Numeric(10,2))

class QualifyingAgentProduct(db.Model):
    __tablename__ = 'qualifying_agent_products'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=True)
    lower_limit = db.Column(db.Integer)
    upper_limit = db.Column(db.Integer)
    price = db.Column(db.Numeric(10,2))

class QualifyingPlaymateProduct(db.Model):
    __tablename__ = 'qualifying_playmate_products'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=True)
    lower_limit = db.Column(db.Integer)
    upper_limit = db.Column(db.Integer)
    price = db.Column(db.Numeric(10,2))

class ForceAgentProduct(db.Model):
    __tablename__ = 'force_agent_products'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=True)
    lower_limit = db.Column(db.Integer)
    upper_limit = db.Column(db.Integer)
    price = db.Column(db.Numeric(10,2))

class ComboProduct(db.Model):
    __tablename__ = 'combo_products'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(256), unique=True)
    price = db.Column(db.Numeric(10,2))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

champion_tag = db.Table('champion_tag',
    db.Column('champion_id', db.Integer, db.ForeignKey('champions.id')),
    db.Column('champion_categry_id', db.Integer, db.ForeignKey('champion_categries.id'))
)

class Champion(db.Model):
    __tablename__ = 'champions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    pic_url = db.Column(db.String(64), unique=True)
    popularity = db.Column(db.Float(10))
    tags = db.relationship('ChampionCategry', secondary=champion_tag, backref='champions')
    
class ChampionCategry(db.Model):
    __tablename__ = 'champion_categries'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=True)

class LevelComparison(db.Model):
    __tablename__ = 'level_comparisons'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=True)
    level = db.Column(db.Integer)
    def __repr__(self):
        return self.label

class CountingParameter(db.Model):
    __tablename__ = 'counting_parameters'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True)
    value = db.Column(db.Float(5))
    def __repr__(self):
        return '<Parameter %r>' % self.key


def compute_peak_agent_money(current:int,expectation:int) -> float:
    return compute_money(current,expectation,PeakAgentProduct)

def compute_qualifying_agent_money(current:int,expectation:int) -> float:
    return compute_money(current=current,expectation=expectation,Model=QualifyingAgentProduct)


def compute_qualifying_playmate_money(current:int,expectation:int) -> float:
    return compute_money(current=current,expectation=expectation,Model=QualifyingPlaymateProduct)

def compute_force_agent_money(current:int,expectation:int) -> float:
    return compute_money(current=current,expectation=expectation,Model=ForceAgentProduct) / 1000

def compute_money(current:int,expectation:int,Model) -> float:
    money:float = 0
    print('current is '+ str(current)+' and expectation is ' + str(expectation))
    queryl = Model.query.filter(Model.lower_limit <= current, Model.upper_limit >= current)
    querys = Model.query.filter(Model.lower_limit > current, Model.upper_limit < expectation)
    queryr = Model.query.filter(Model.lower_limit <= expectation, Model.upper_limit >= expectation)
    products = queryl.union_all(querys, queryr).order_by(Model.lower_limit).all()

    print('final list is' + str(products))

    for product in products:
        if current < expectation:
            if expectation > product.upper_limit:
                money += (product.upper_limit - current) * product.price
            else:
                money += (expectation - current) * product.price
            current = product.upper_limit
        else:
            break
    return money
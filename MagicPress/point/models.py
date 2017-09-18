from MagicPress import db

class Point(db.model):
    __tablename__ = 'points'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    abstract = db.Column(db.Text())
    create_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    state = db.Column(db.Boolean, default=True)
    categories = db.relationship('Category', backref='picture')

    def __repr__(self):
        return self.name
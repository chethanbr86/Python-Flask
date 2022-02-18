from myproject import db

class Playstation(db.Model):
    __tablename__ = 'games_played'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    game_stat = db.relationship('Game_Status',backref='game',uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.game_stat:
            return f'Game id is : {self.id}, game name is {self.name} and status is {self.game_stat.name}'
        else:
            return f'Game id is : {self.id}, game name is {self.name} and status is None yet!'

class Game_Status(db.Model):
    __tablename__ = 'status_games'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    stat_id = db.Column(db.Integer, db.ForeignKey('games_played.id'))

    def __init__(self,name,stat_id):
        self.name = name
        self.stat_id = stat_id

    def __repr__(self):        
        return f'status is {self.stat_id, self.name}'
from task_model import db

class Mytodo_List(db.Model):
    __tablename__ = 'TODOLIST'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.Text)
    task_status = db.Column(db.Text)

    def __init__(self, task_name, task_status):
        self.task_name = task_name
        self.task_status = task_status

    # def __repr__(self):        
    #     # flash(f'Task: {self.task_name} added')
    #     return  f'ID: {self.id}, Your new task is: {self.task_name} and its status is: {self.task_status}'  

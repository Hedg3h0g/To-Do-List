# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
today = datetime.today().date()
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='task')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

while True:
    print("""
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    x = int(input())

    if x == 1:
        print("Today", today.day, today.strftime('%b') + ":")
        rows = session.query(Table).filter(Table.deadline == today).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i].task}")

    if x == 2:
        rows = session.query(Table).filter(Table.deadline == today).all()
        temp = today

        for n in range(7):
            print(weekdays[temp.weekday()], temp.day,
                      temp.strftime('%b') + ":")
            if len(rows) == 0:
                print("Nothing to do!")
                print()
            else:
                for i in range(len(rows)):
                    print(f"{i + 1}. {rows[i].task}")
                print()

            temp = temp + timedelta(days=1)
            rows = session.query(Table).filter(Table.deadline == temp).all()

    if x == 3:
        print("All tasks:")
        rows = session.query(Table).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}.")

    if x == 4:
        print("Missed tasks:")
        rows = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        if len(rows) == 0:
            print("Nothing is missed!")
        else:
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}.")

    if x == 5:
        print("Enter task")
        s = input()
        print("Enter deadline")
        d = datetime.strptime(input(), "%Y-%m-%d")
        new_row = Table(task=s, deadline=d)
        session.add(new_row)
        session.commit()
        print("The task has been added!")

    if x == 6:
        print("Chose the number of the task you want to delete:")
        rows = session.query(Table).order_by(Table.deadline).all()
        if len(rows) == 0:
            print("Nothing to delete!")
        else:
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}.")
        dl = int(input())
        rows = rows[dl - 1]
        session.delete(rows)
        session.commit()
        print("The task has been deleted!")

    if x == 0:
        print("Bye!")
        break

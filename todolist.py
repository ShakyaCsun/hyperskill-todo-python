from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
# A database file is created with create_engine() method
# `todo.db` is the database file name
# check_same_thread=False allows connecting to database from another thread
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

# All model classes should inherit from the class `DeclarativeMeta` returned by declarative_base()
Base = declarative_base()


# All rows in table are objects of class Tasks.
class Tasks(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date)

    def __repr__(self):
        return self.task

    def get_details(self):
        return self.task, self.deadline


# This creates all the classes derived from Base i.e. class returned by declarative_base()
Base.metadata.create_all(engine)

# To access the database and store data in it, we need to create a session
Session = sessionmaker(bind=engine)
session = Session()


def add_row(task, deadline):
    # Add a row in database
    new_row = Tasks(task=task, deadline=deadline)
    session.add(new_row)
    session.commit()


def query_db(filter_date=None):
    if filter_date:
        rows = session.query(Tasks).filter(Tasks.deadline == filter_date).order_by(Tasks.deadline).all()
    else:
        # Query all rows of the database class/table
        rows = session.query(Tasks).order_by(Tasks.deadline).all()
    return rows


def task_lists(tasks):
    if len(tasks) == 0:
        print('Nothing to do!')
    else:
        for i in range(len(tasks)):
            print(f'{i + 1}) {tasks[i]}')
    print()


def task_deadlines(tasks, default_message='No tasks'):
    if len(tasks) > 0:
        for i in range(len(tasks)):
            todo, deadline = tasks[i].get_details()
            print(f'{i + 1}) {todo}. {deadline.day} {deadline.strftime("%b")}')
    else:
        print(default_message)


# Option 1
def today_tasks():
    today = datetime.today().date()
    print(f"Today {today.day} {today.strftime('%b')}")
    tasks = query_db(filter_date=today)
    task_lists(tasks)


# Option 2
def weeks_tasks():
    today = datetime.today().date()
    for i in range(7):
        date = today + timedelta(days=i)
        print(f"{days[date.weekday()]} {date.day} {date.strftime('%b')}:")
        tasks = query_db(filter_date=date)
        task_lists(tasks)
    print()


# Option 3
def all_tasks():
    tasks = query_db()
    print('All tasks:')
    task_deadlines(tasks)
    print()


# Option 4
def missed_tasks():
    tasks = session.query(Tasks).filter(Tasks.deadline < datetime.today()).order_by(Tasks.deadline).all()
    print('Missed tasks:')
    task_deadlines(tasks, default_message='Nothing is missed!')
    print()


# Option 5
def add_task():
    task = input('Enter task\n')
    correct_format = False
    while not correct_format:
        try:
            deadline = input('Enter deadline\n')
            deadline = datetime.strptime(deadline, '%Y-%m-%d')
            correct_format = True
            add_row(task, deadline)
        except ValueError:
            print('Deadline should be a valid date in YYYY-MM-DD format')

    print('The task has been added!')
    print()


# Option 6
def delete_task():
    tasks = query_db()
    print('Choose the number of the task you want to delete:')
    task_deadlines(tasks, 'Nothing to delete')
    if len(tasks) > 0:
        to_delete = take_int_input('Choose the number of the task you want to delete:') - 1
        session.delete(tasks[to_delete])
        session.commit()
    print()


def take_int_input(message='Enter a integer input.'):
    while True:
        user_input = input()
        if user_input.isnumeric():
            user_input = int(user_input)
            return user_input
        else:
            print(message)


def menu():
    is_running = True
    while is_running:
        print('1) Today\'s tasks')
        print('2) Week\'s tasks')
        print('3) All tasks')
        print('4) Missed tasks')
        print('5) Add task')
        print('6) Delete task')
        print('0) Exit')

        user_input = take_int_input()
        if user_input == 1:
            today_tasks()
        elif user_input == 2:
            weeks_tasks()
        elif user_input == 3:
            all_tasks()
        elif user_input == 4:
            missed_tasks()
        elif user_input == 5:
            add_task()
        elif user_input == 6:
            delete_task()
        elif user_input == 0:
            print('\nBye!')
            is_running = False
        else:
            print('Enter a valid input.')


if __name__ == '__main__':
    menu()

from sqlalchemy import func, desc, select, and_

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def select_one():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    :return: list[dict]
    """
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result


def select_two(discipline_id: int):
    r = session.query(Discipline.name,
                      Student.fullname,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()
    return r

"""
select s.id, s.fullname, g.grade, g.date_of
from grades g
  inner join students s on s.id = g.student_id
where g.discipline_id = 2
  and s.group_id = 2
  and g.date_of = (select max(date_of) -- находим последнее занятие для данной группы по данному предмету
                   from grades g2
                     inner join students s2 on s2.id = g2.student_id
                   where g2.discipline_id = g.discipline_id
                     and s2.group_id = s.group_id);

"""

def select_three(discipline_id: int):
    r = session.query(Group.name,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Group.id) \
        .order_by(desc('avg_grade')) \
        .all()
    return r

def select_four():
    r = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .limit(1).all()
    return r

def select_five(teacher_id: int):
    r = session.query(Discipline.name,
                      Teacher.fullname,
                      ) \
        .select_from(Discipline) \
        .join(Teacher) \
        .filter(Teacher.id == teacher_id) \
        .all()
    return r

def select_six(group_id: int):
    r = session.query(Group.name,
                      Student.fullname,
                      ) \
        .select_from(Student) \
        .join(Group) \
        .filter(Group.id == group_id) \
        .all()
    return r

def select_seven(discipline_id: int, group_id: int):
    r = session.query(Group.name,
                      Discipline.name,
                      Student.fullname,
                      Grade.grade
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(Discipline.id == discipline_id) \
        .filter(Group.id == group_id) \
        .all()
    return r

def select_eight(teacher_id: int):
    r = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .join(Teacher) \
        .filter(Teacher.id == teacher_id) \
        .all()
    return r

def select_nine(student_id: int):
    r = session.query(Discipline.name    
                      #   Student.fullname,                  
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Student.id == student_id) \
        .group_by(Discipline.id) \
        .all()
    return r

def select_ten(student_id: int, teacher_id: int):
    r = session.query(Discipline.name,
                    #   Student.fullname,
                    #   Teacher.fullname
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(Student.id == student_id) \
        .filter(Teacher.id == teacher_id) \
        .group_by(Discipline.name) \
        .all()
    return r

def select_eleven(student_id: int, teacher_id: int):
    r = session.query(
                    #   Student.fullname,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(Student.id == student_id) \
        .filter(Teacher.id == teacher_id) \
        .group_by(Student.id) \
        .all()
    return r

def select_twelve(discipline_id, group_id):
    subquery = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == discipline_id, Group.id == group_id)
    ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery())

    r = session.query(Discipline.name,
                      Student.fullname,
                      Group.name,
                      Grade.date_of,
                      Grade.grade
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group)\
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery)) \
        .order_by(desc(Grade.date_of)) \
        .all()
    return r


if __name__ == '__main__':
    print(select_one())
    print(select_two(1))
    print(select_three(1))
    print(select_four())
    print(select_five(1))
    print(select_six(1))
    print(select_seven(1, 2))
    print(select_eight(2))
    print(select_nine(23))
    print(select_ten(23, 2))
    print(select_eleven(1, 1))
    print(select_twelve(1, 2))
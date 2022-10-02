class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        name = f"Имя: {self.name}\nФамилия: {self.surname}"
        if len(self.courses_in_progress) > 0:
            progress = f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}"
        else:
            progress = 'Курсы в процессе изучения: нет'
        if len(self.finished_courses) > 0:
            finish = f"Завершенные курсы: {', '.join(self.finished_courses)}"
        else:
            finish = 'Завершенные курсы: нет'
        if self._average_grade() > 0:
            average = f"Средняя оценка за домашние задания: {self._average_grade()}"
        else:
            average = f"Средняя оценка за домашние задания: {self.name} {self.surname}" \
                      f" не имеет оценок за домашние задания"
        return f"{name}\n{average}\n{progress}\n{finish}"

    def __lt__(self, other):
        if isinstance(other, Student):
            return self._average_grade() < other._average_grade()
        else:
            raise TypeError(f"{other} not in class Student")

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and
                course in lecturer.courses_attached and
                course in self.courses_in_progress and
                0 < grade < 11
        ):
            if course in lecturer.grades_dict:
                lecturer.grades_dict[course] += [grade]
            else:
                lecturer.grades_dict[course] = [grade]
        else:
            raise ValueError("You can rate from 1 to 10"
                             " and you need to attend this lecture")

    def _average_grade(self):
        sum_grades = 0
        count_grades = 0
        for value in self.grades.values():
            for grade in value:
                sum_grades += grade
                count_grades += 1
        if count_grades > 0:
            return round((sum_grades / count_grades), 1)
        else:
            return 0


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        if isinstance(self, Reviewer):
            res = f"Имя: {self.name}\nФамилия: {self.surname}"
            return res
        elif isinstance(self, Lecturer):
            if self._average_grade() > 0:
                average = f"Средняя оценка за лекции: {self._average_grade()}"
            else:
                average = f"Средняя оценка за лекции: {self.name} {self.surname}" \
                          f" не имеет оценок за лекции"
            res = f"Имя: {self.name}\nФамилия: {self.surname}\n{average}"
            return res
        else:
            return object.__str__(self)


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades_dict = {}

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self._average_grade() < other._average_grade()
        else:
            raise TypeError(f"{other} not in class Lecturer")

    def _average_grade(self):
        sum_grades = 0
        count_grades = 0
        for value in self.grades_dict.values():
            for grade in value:
                sum_grades += grade
                count_grades += 1
        if count_grades > 0:
            return round((sum_grades / count_grades), 1)
        else:
            return 0


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and
                course in student.courses_in_progress and
                course in self.courses_attached
        ):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            raise NameError(f"{self.name} {self.surname} can't rate this course")


def average_all_hw(students_list, course):
    average_grade = 0
    count_grade = 0
    for student in students_list:
        if course in student.grades:
            for grade in student.grades[course]:
                average_grade += grade
                count_grade += 1
    if count_grade > 0:
        res = round((average_grade / count_grade), 1)
        return f'Средняя оценка {res} за домашние работы по курсу {course}'
    else:
        return f"Студенты не получали оценок по курсу {course}"


def average_all_lect(lecturers_list, course):
    average_grade = 0
    count_grade = 0
    for lecturer in lecturers_list:
        if course in lecturer.grades_dict:
            for grade in lecturer.grades_dict[course]:
                average_grade += grade
                count_grade += 1
    if count_grade > 0:
        res = round((average_grade / count_grade), 1)
        return f'Средняя оценка {res} за лекции по курсу {course}'
    else:
        return f"Лекторы не получали оценок по курсу {course}"


# student1 = Student('SName1', 'SSurname1', 'SMale1')
# student2 = Student('SName2', 'SSurname2', 'SFemale2')
#
# mentor1 = Mentor('MName1', 'MSurname1')
# mentor2 = Mentor('MName2', 'MSurname2')
#
# lecturer1 = Lecturer('LName1', 'LSurname1')
# lecturer2 = Lecturer('LName2', 'LSurname2')
#
# reviewer1 = Reviewer('RName1', 'RSurname1')
# reviewer2 = Reviewer('RName2', 'RSurname2')
#
# student1.finished_courses = ['Python', 'Java', 'PHP']
# student1.courses_in_progress = ['React', 'SQL', 'Git', 'Java']
#
# student2.finished_courses = ['React', 'SQL', 'Git']
# student2.courses_in_progress = ['Python', 'Java', 'PHP']
#
# mentor1.courses_attached = ['Python']
# mentor2.courses_attached = ['Git']
#
# lecturer1.courses_attached = ['Python', 'SQL', 'Git']
# lecturer2.courses_attached = ['SQL', 'Python']
#
# reviewer1.courses_attached = ['Git', 'React']
# reviewer2.courses_attached = ['SQL', 'PHP', 'Java']
#
# student1.rate_lecture(lecturer1, 'SQL', 5)
# student1.rate_lecture(lecturer1, 'SQL', 9)
# student2.rate_lecture(lecturer1, 'Python', 8)
# student2.rate_lecture(lecturer1, 'Python', 6)
# student1.rate_lecture(lecturer2, 'SQL', 9)
# student1.rate_lecture(lecturer2, 'SQL', 10)
# student2.rate_lecture(lecturer2, 'Python', 4)
#
# reviewer1.rate_hw(student1, 'Git', 8)
# reviewer1.rate_hw(student1, 'Git', 4)
# reviewer1.rate_hw(student1, 'React', 6)
# reviewer1.rate_hw(student1, 'React', 7)
# reviewer2.rate_hw(student2, 'PHP', 9)
# reviewer2.rate_hw(student2, 'PHP', 8)
# reviewer2.rate_hw(student2, 'Java', 8)
# reviewer2.rate_hw(student2, 'Java', 9)
# reviewer2.rate_hw(student2, 'Java', 8)
# reviewer2.rate_hw(student1, 'Java', 4)
# reviewer2.rate_hw(student1, 'Java', 5)
# reviewer2.rate_hw(student1, 'Java', 3)
#
# print(student1)
# print('_____')
# print(student2)
# print('_____')
# print(mentor1)
# print('_____')
# print(lecturer1)
# print('_____')
# print(lecturer2)
# print('_____')
# print(reviewer2)
# print('_____')
#
# print(lecturer1 > lecturer2)
# print(lecturer2 > lecturer1)
# print(student1 > student2)
# print(student2 > student1)
#
# print(average_all_hw([student1, student2], 'Java'))
# print(average_all_hw([student1, student2], 'React'))
# print(average_all_hw([student1, student2], 'Git'))
# print(average_all_lect([lecturer1, lecturer2], 'Python'))
# print(average_all_lect([lecturer1, lecturer2], 'React'))
# print(average_all_lect([lecturer1, lecturer2], 'SQL'))

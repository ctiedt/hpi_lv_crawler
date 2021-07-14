#!/usr/bin/python
from course import Course
from crawler import crawl
import pickle
import sys


class CourseFilter:
    def __init__(self, filter_fun):
        self.filter_fun = filter_fun

    def __call__(self, course):
        return self.filter_fun(course)

    def __and__(self, other):
        def and_fun(c): return self.filter_fun(c) and other.filter_fun(c)
        return CourseFilter(and_fun)

    def __or__(self, other):
        def or_fun(c): return self.filter_fun(c) or other.filter_fun(c)
        return CourseFilter(or_fun)


IS_MA_ITSE = CourseFilter(
    lambda course: 'IT-Systems Engineering MA' in course.courses_of_study)

IS_LECTURE = CourseFilter(lambda course: course.kind.startswith('Vorlesung'))


def main():
    sys.setrecursionlimit(10000)
    if len(sys.argv) < 2:
        with open('courses.pkl', 'rb') as file:
            courses = pickle.load(file)
    else:
        url = sys.argv[1]
        courses = crawl(url)
        with open('courses.pkl', 'wb+') as file:
            pickle.dump(courses, file)
    for course in filter(IS_MA_ITSE & IS_LECTURE, courses):
        print(course)


if __name__ == "__main__":
    main()

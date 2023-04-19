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
        def and_fun(c):
            return self.filter_fun(c) and other.filter_fun(c)

        return CourseFilter(and_fun)

    def __or__(self, other):
        def or_fun(c):
            return self.filter_fun(c) or other.filter_fun(c)

        return CourseFilter(or_fun)


IS_MA_ITSE = CourseFilter(
    lambda course: "IT-Systems Engineering MA" in course.courses_of_study
)

IS_LECTURE = CourseFilter(lambda course: "Vorlesung" in course.kind)

IS_SEMINAR = CourseFilter(lambda course: "Seminar" in course.kind)

IS_PROJECT = CourseFilter(lambda course: "Projekt" in course.kind)


def HAS_MODULE(module: str):
    return CourseFilter(
        lambda course: any(m.startswith(module) for m in course.modules)
    )


def print_as_md_table(courses: list[Course]):
    print("| Name | Lehrform | ECTS | Module |")
    print("|------|----------|------|--------|")
    for course in courses:
        modules = ", ".join(
            filter(
                lambda module: module is not None,
                course.modules,
            )
        )
        print(f"| {course.name} | {course.kind} | {course.ects} | {modules} |")


def main():
    sys.setrecursionlimit(100000)
    if len(sys.argv) < 2:
        with open("courses.pkl", "rb") as file:
            courses = pickle.load(file)
    elif sys.argv[1] == "load":
        with open(sys.argv[2], "rb") as file:
            courses = pickle.load(file)
    else:
        url = sys.argv[1]
        courses = crawl(url)
        cache = "courses-" + url.split("/")[-1].replace(".html", "") + ".pkl"
        with open(cache, "wb+") as file:
            pickle.dump(courses, file)

    print_as_md_table(courses)


if __name__ == "__main__":
    main()

from dataclasses import dataclass


@dataclass
class Course:
    name: str
    lecturers: list[str]
    kind: str
    ects: int
    courses_of_study: list[str]
    modules: list[str]

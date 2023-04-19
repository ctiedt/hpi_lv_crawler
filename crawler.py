from course import Course
import urllib.request as request
from bs4 import BeautifulSoup
import sys


def crawl(url: str) -> list[Course]:
    courses = []
    response = request.urlopen(url)
    if response.status != 200:
        exit("Request failed")

    soup = BeautifulSoup(response.read(), "html.parser")
    for item in soup.find_all("tr"):
        courselink = item.find(class_="courselink")["href"]
        try:
            course = process_courselink(courselink)
            courses.append(course)
        except Exception:
            print(f"Could not parse course {courselink}", file=sys.stderr)

    return courses


def parse_lecturers(candidates: list) -> list[str]:
    lecturers = []
    for candidate in candidates:
        link = candidate.find("a")
        if link is not None and not link.string.strip().startswith("https://hpi.de"):
            lecturers.append(link.string)
    return lecturers


def process_courselink(link: str) -> Course:
    response = request.urlopen("https://hpi.de" + link)
    if response.status != 200:
        exit("Request failed")

    soup = BeautifulSoup(response.read(), "html.parser")
    name = soup.find("h1").string

    lecturers = parse_lecturers(soup.find_all("i"))

    info = soup.find(class_="tx-ciuniversity-course-general-info")
    if info is None:
        raise Exception("Invalid Course Page")
    lis = [li.string.strip() for li in info.find_all("li")]
    kind = "".join(next(filter(lambda li: li.startswith("Lehrform"), lis)).split()[1:])
    ects = int(next(filter(lambda li: li.startswith("ECTS"), lis)).split()[-1])
    courses_of_study = [
        cos.string.strip() for cos in soup.find_all(class_="tx_dscclipclap_header")
    ]
    cos_modules = [
        cos.find_all("li") for cos in soup.find_all(class_="tx_dscclipclap_content")
    ]
    modules = []
    for cos in cos_modules:
        for module in cos:
            mod = list(module.strings)[-1].strip()
            if mod != "":
                modules.append(mod.split(" ")[0])

    return Course(name, lecturers, kind, ects, courses_of_study, modules)

import os
import json
from collections import Counter


# ==========================
# OOP: Course Class
# ==========================

class Course:

    def __init__(self, code, name, details):
        self.code = code
        self.name = name
        self.details = details


    def get_department(self):
        return self.details.get(
            "Department",
            "Unknown"
        )


    def get_duration(self):
        return self.details.get(
            "Duration",
            "Unknown"
        )


    def display(self):

        print("-" * 60)
        print("Course Code :", self.code)
        print("Course Name :", self.name)
        print("Department  :", self.get_department())
        print("Duration    :", self.get_duration())


 
# ==========================
# Read JSON File
# ==========================

def load_courses(filename):

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)


    courses = []


    for item in data:

        course = Course(
            item["course_code"],
            item["course_name"],
            item["course_details"]
        )

        courses.append(course)


    return courses



# ==========================
# Generate Report
# ==========================

def generate_report(courses):


    print("=" * 60)
    print("              FCIT COURSE REPORT")
    print("=" * 60)


    print(
        "Total Courses:",
        len(courses)
    )


    print("\nCourse List")
    print("-" * 60)


    for index, course in enumerate(
        courses,
        start=1
    ):

        print(
            f"{index}. {course.name}"
        )


    print("\nCourse Details")


    for course in courses:

        course.display()



    # Department statistics

    departments = Counter()


    for course in courses:

        departments[
            course.get_department()
        ] += 1



    print("\nDepartment Summary")
    print("-" * 60)


    for dept, total in departments.items():

        print(
            dept,
            ":",
            total
        )



    # Save TXT Report

    with open(
        "c:\\xampp\\htdocs\\intern\\week6\\report.txt",
        "w",
        encoding="utf-8"
    ) as file:


        file.write(
            "FCIT COURSE REPORT\n"
        )

        file.write(
            "=" * 60 + "\n"
        )


        file.write(
            f"Total Courses: {len(courses)}\n\n"
        )


        file.write(
            "Course List\n"
        )


        for index, course in enumerate(
            courses,
            start=1
        ):

            file.write(
                f"{index}. {course.name}\n"
            )


        file.write(
            "\nDepartment Summary\n"
        )


        for dept, total in departments.items():

            file.write(
                f"{dept}: {total}\n"
            )


    print(
        "\nReport generated: report.txt"
    )



# ==========================
# Main Program (CLI)
# ==========================

if __name__ == "__main__":


    filename = os.path.join(
    os.path.dirname(__file__),
    "fcit_data.json"
    )

    courses = load_courses(
        filename
    )


    generate_report(
        courses
    )
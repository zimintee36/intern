import os
import json
import requests
from bs4 import BeautifulSoup


# ==========================
# 课程网页
# ==========================

courses = [
    ("bcs", "https://www.newera.edu.my/course_details.php?acalevel=1&course=39"),
    ("bse", "https://www.newera.edu.my/course_details.php?acalevel=1&course=29"),
    ("dcs", "https://www.newera.edu.my/course_details.php?acalevel=3&course=38"),
    ("dit", "https://www.newera.edu.my/course_details.php?acalevel=3&course=5"),
    ("fia", "https://www.newera.edu.my/course_details.php?acalevel=2&course=49")
]


headers = {
    "User-Agent": "Mozilla/5.0"
}


# ==========================
# 建立资料夹
# ==========================

save_dir = "py-week4"

os.makedirs(
    save_dir,
    exist_ok=True
)


fcit_table = []


# ==========================
# 抓取 Tab 内容
# ==========================

def get_tab_content(soup, tab_name):

    data = []

    tab = soup.find(
        "div",
        id=lambda x: x and x.startswith(tab_name)
    )


    if tab:

        # 删除图片内容
        for img in tab.find_all("img"):
            img.decompose()


        # 需要过滤的文字
        remove_words = [
            "Course Introduction",
            "Programme Modules *",
            "Minimum Entry Requirement",
            "Career Prospects",
            "Partnerships:"
        ]


        for tag in tab.find_all(
            [
                "h5",
                "p",
                "li"
            ]
        ):

            text = tag.get_text(
                " ",
                strip=True
            )


            if (
                text
                and text not in data
                and text not in remove_words
            ):

                data.append(text)


    return data



# ==========================
# 开始抓取
# ==========================

for index, (course_code, url) in enumerate(
        courses,
        start=1
):

    print(
        f"\n===== 抓取 {course_code} ====="
    )


    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )


        response.raise_for_status()

        response.encoding = "utf-8"


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


    except Exception as e:

        print(
            "连接失败:",
            e
        )

        continue



    # ==========================
    # 建立课程资料夹
    # ==========================

    course_dir = os.path.join(
        save_dir,
        course_code,
        "course"
    )


    os.makedirs(
        course_dir,
        exist_ok=True
    )



    # ==========================
    # 保存 course.txt
    # ==========================

    txt_file = os.path.join(
        course_dir,
        "course.txt"
    )


    seen = set()


    with open(
        txt_file,
        "w",
        encoding="utf-8"
    ) as f:


        for tag in soup.find_all(
            [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "p",
                "li"
            ]
        ):


            text = tag.get_text(
                " ",
                strip=True
            )


            if (
                text
                and text not in seen
            ):

                seen.add(text)

                f.write(
                    text + "\n"
                )


    print(
        "course.txt 完成"
    )



    # ==========================
    # Course Details
    # ==========================

    course_details = {}

    course_name = ""


    table = soup.find(
        "table",
        class_="table"
    )


    if table:


        for row in table.find_all("tr"):


            cols = row.find_all(
                [
                    "th",
                    "td"
                ]
            )


            if len(cols) == 2:


                key = cols[0].get_text(
                    " ",
                    strip=True
                )


                value = cols[1].get_text(
                    " ",
                    strip=True
                )


                # Award 改成 course_name
                if key == "Award:":

                    course_name = value

                else:

                    course_details[key] = value



    # ==========================
    # 四个 Tab
    # ==========================

    course_intro = get_tab_content(
        soup,
        "tab1"
    )


    programme_modules = get_tab_content(
        soup,
        "tab2"
    )


    entry_requirement = get_tab_content(
        soup,
        "tab3"
    )


    career_prospects = get_tab_content(
        soup,
        "tab4"
    )



    # ==========================
    # 存入 JSON
    # ==========================

    fcit_table.append(

        {

            "course_code":
                course_code,


            "course_name":
                course_name,


            "course_details":
                course_details,


            "course_introduction":
                course_intro,


            "programme_modules":
                programme_modules,


            "entry_requirement":
                entry_requirement,


            "career_prospects":
                career_prospects,


            "source_url":
                url

        }

    )


    print(
        course_code,
        "完成"
    )



# ==========================
# 输出 JSON
# ==========================

json_file = os.path.join(
    save_dir,
    "fcit_data.json"
)


with open(
    json_file,
    "w",
    encoding="utf-8"
) as f:


    json.dump(
        fcit_table,
        f,
        ensure_ascii=False,
        indent=4
    )



print(
    "\n===== 全部完成 ====="
)


print(
    "JSON:",
    os.path.abspath(json_file)
)
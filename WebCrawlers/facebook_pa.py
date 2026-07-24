from playwright.sync_api import sync_playwright
import requests
import json
import os
import time


# ==========================
# 设置区域
# ==========================

PAGE_URL = "https://www.facebook.com/NEUCFCIT"

LOGIN_FILE = "facebook_login.json"

POST_FOLDER = "postlist"
IMAGE_FOLDER = "facebook_images"


os.makedirs(POST_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)



# ==========================
# 下载图片
# ==========================

def download_image(url, filename):

    try:

        r = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        if r.status_code == 200:

            with open(
                filename,
                "wb"
            ) as f:
                f.write(r.content)

            return True


    except Exception as e:

        print(
            "下载图片失败:",
            e
        )


    return False



# ==========================
# 保存JSON
# ==========================

def save_json(data, number):

    filename = (
        f"{POST_FOLDER}/"
        f"posts_{number:03}.json"
    )


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


    print(
        "保存:",
        filename
    )



# ==========================
# 主程序
# ==========================

with sync_playwright() as p:


    browser = p.chromium.launch(
        headless=False
    )


    # 读取登录状态
    context = browser.new_context(
        storage_state=LOGIN_FILE
    )


    page = context.new_page()


    print(
        "打开 Facebook..."
    )


    page.goto(
        PAGE_URL,
        wait_until="domcontentloaded"
    )


    page.wait_for_timeout(
        5000
    )


    print(
        "页面:",
        page.title()
    )


    collected = []

    json_number = 1

    processed = set()

    no_new_count = 0

    old_total = 0



    while True:


        # --------------------------
        # 滚动加载帖子
        # --------------------------

        page.mouse.wheel(
            0,
            8000
        )


        page.wait_for_timeout(
            4000
        )


        posts = page.locator(
            'div[role="article"]'
        )


        total = posts.count()


        print(
            "发现帖子:",
            total
        )


        if total == old_total:

            no_new_count += 1

        else:

            no_new_count = 0


        old_total = total



        if no_new_count >= 5:

            print(
                "没有更多帖子"
            )

            break



        # --------------------------
        # 读取帖子
        # --------------------------

        for i in range(total):


            if i in processed:
                continue



            post = posts.nth(i)



            item = {

                "id":
                i + 1,

                "text":
                "",

                "images":
                []

            }



            # 帖子文字

            try:

                item["text"] = (
                    post.inner_text()
                )


            except:

                pass



            # 图片

            imgs = post.locator(
                "img"
            )


            img_total = imgs.count()



            for j in range(img_total):


                src = (
                    imgs
                    .nth(j)
                    .get_attribute("src")
                )



                if (
                    src
                    and
                    (
                    "scontent" in src
                    or
                    "fbcdn" in src
                    )
                ):


                    filename = (

                        f"{IMAGE_FOLDER}/"
                        f"post_{i+1}_"
                        f"{j+1}.jpg"

                    )


                    if download_image(
                        src,
                        filename
                    ):


                        item["images"].append(
                            filename
                        )



            collected.append(
                item
            )


            processed.add(i)



            print(
                "完成帖子:",
                i + 1
            )



            # 每10篇保存

            if len(collected) == 10:


                save_json(
                    collected,
                    json_number
                )


                json_number += 1

                collected = []



    # --------------------------
    # 保存剩余帖子
    # --------------------------

    if collected:


        save_json(
            collected,
            json_number
        )



    browser.close()



print(
    "全部完成"
)
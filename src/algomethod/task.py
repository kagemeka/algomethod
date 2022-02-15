from __future__ import annotations

import dataclasses
import json

import requests

import algomethod._scrape
import algomethod.constant

_TASKS_URL = f"{algomethod.constant._SITE_URL}/tasks"
_LECTURE_URL = f"{algomethod.constant._SITE_URL}/lecture_groups"

# async def _get_tasks_page(
#     session: aiohttp.ClientSession,
# ) -> aiohttp.ClientResponse:
#     return await session.get(_TASKS_URL)


def _get_tasks_page(
    # driver: selenium.webdriver.remote.webdriver.WebDriver,
) -> requests.Response:
    # driver.get(_TASKS_URL)
    # time.sleep(1)
    # return typing.cast(str, driver.page_source)
    return requests.get(_TASKS_URL)


@dataclasses.dataclass
class Lecture:
    id: int
    title: str


def _scrape_lectures(html: str) -> list[Lecture]:
    soup = algomethod._scrape._parse_html(html)
    datas = json.loads(soup.find(id="__NEXT_DATA__").text)
    return [
        Lecture(**lecture)
        for lecture in datas["props"]["pageProps"]["lecture_groups"]
    ]


def _get_lecture_page(lecture_id: int) -> requests.Response:
    return requests.get(f"{_LECTURE_URL}/{lecture_id}")


def _scrape_task_ids(html: str) -> list[int]:
    soup = algomethod._scrape._parse_html(html)
    datas = json.loads(soup.find(id="__NEXT_DATA__").text)
    lectures = datas["props"]["pageProps"]["lgs"]["lectures"]
    task_ids = []
    for lecture in lectures:
        task_ids.extend([int(task["id"]) for task in lecture["tasks"]])
    return task_ids


def fetch_task_ids() -> list[int]:
    response = _get_tasks_page()
    lectures = _scrape_lectures(response.text)
    task_ids = []
    for lecture in lectures:
        response = _get_lecture_page(lecture.id)
        task_ids.extend(_scrape_task_ids(response.text))
    task_ids.sort()
    return task_ids


if __name__ == "__main__":
    task_ids = fetch_task_ids()
    print(task_ids)

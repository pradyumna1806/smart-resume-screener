import asyncio
import requests


async def main():
    with open("../jpmorgan_jd.txt", "r", encoding="utf-8") as file:
        jd = file.read()

    response = requests.post(
        "http://127.0.0.1:8000/api/jobs/extract",
        json={"description": jd},
    )

    print("Status:", response.status_code)
    print(response.text)


asyncio.run(main())
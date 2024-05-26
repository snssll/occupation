import requests
import pandas as pd
from tqdm import tqdm
import pandas as pd
import os
from dotenv import load_dotenv
import time

load_dotenv()

apikey = os.getenv("OPENAI_API_KEY")
openai_url = "https://api.openai.com/v1/chat/completions"

system_prompt = ""
user_prompt_without_tail = ""

with open("system_prompt.txt", "r") as f:
    system_prompt = f.read()

with open("user_prompt.txt", "r") as f:
    user_prompt_without_tail = f.read()

messages_template = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "todo"},
]


def make_user_content(title, task):
    occupation = "Occupation: " + title
    task = "Task: " + task
    return user_prompt_without_tail + "\n" + occupation + "\n" + task


def make_messages(title, task):
    messages = messages_template.copy()
    messages[1]["content"] = make_user_content(title, task)
    return messages


def get_response(title, task):
    response = requests.post(
        openai_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {apikey}",
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": make_messages(title, task),
            "temperature": 0,
            "max_tokens": 1024,
            "top_p": 1,
        },
    )
    data = response.json()
    return data["choices"][0]["message"]["content"]


def res_2_file(index, title, task):
    try:
        res = get_response(title, task)
        with open(f"output/{index}.txt", "a") as f:
            f.write(res)
    except Exception as e:
        print(f"{index} error: {e}")
        print("sleep 60s")
        time.sleep(60)
        try:
            res = get_response(title, task)
            with open(f"output/{index}.txt", "a") as f:
                f.write(res)
        except Exception as e:
            print(f"{index} error: {e} 重试失败")


def main():
    df = pd.read_csv("tasks.csv")
    df["index"] = range(len(df))

    file_list = os.listdir("./output/")
    file_list = [int(file.split(".")[0]) for file in file_list if file.endswith(".txt")]
    file_list = set(file_list)

    for i in tqdm(range(len(df))):
        if i not in file_list:
            res_2_file(df["index"][i], df["Title"][i], df["Task"][i])


if __name__ == "__main__":
    main()

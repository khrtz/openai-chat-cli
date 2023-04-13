import openai
import json
import uuid
import os

LOGS_DIRECTORY = "logs"
PRICE_PER_TOKEN = 0.002


def load_api_key():
    with open("secrets.json", "r") as f:
        secrets = json.load(f)
        return secrets["openai_api_key"]


def calculate_cost(amount_tokens, price_per_token):
    return amount_tokens * price_per_token


def generate_title(chat, num_messages=3, max_length=20):
    last_messages = [msg["content"] for msg in chat[-num_messages:] if msg["role"] == "user"]
    title = " / ".join(last_messages)
    return title[:max_length] + "..." if len(title) > max_length else title


def create_logs_directory():
    if not os.path.exists(LOGS_DIRECTORY):
        os.makedirs(LOGS_DIRECTORY)


def save_chat_log(conversation_name, chat):
    with open(f"{LOGS_DIRECTORY}/{conversation_name}.json", "w") as f:
        json.dump(chat, f)


def select_conversation():
    choice = input("新しい会話を開始しますか？ (y/n) ")
    if choice.lower() == "y":
        conversation_id = str(uuid.uuid4())
        conversation_name = f"conversation-{conversation_id}"
        chat = []
    else:
        logs = [f for f in os.listdir(LOGS_DIRECTORY) if f.endswith(".json")]
        if not logs:
            print("利用可能なログファイルがありません。")
            return None
        print("利用可能なログファイル:")
        for i, log_file in enumerate(logs):
            with open(os.path.join(LOGS_DIRECTORY, log_file), "r") as f:
                chat = json.load(f)
                title = generate_title(chat)
                print(f"{i+1}. {title}")
        index = int(input("どのログファイルを続けますか？ (番号を入力): "))
        conversation_name = logs[index-1].split(".")[0]
        with open(os.path.join(LOGS_DIRECTORY, conversation_name + ".json"), "r") as f:
            chat = json.load(f)
    return conversation_name, chat


def main():
    openai.api_key = load_api_key()
    create_logs_directory()
    conversation_name, chat = select_conversation()
    amount_tokens = 0

    setting = input("ChatGPTに役割や設定を与えますか？ y/n\n")
    if setting == "y" or setting == "Y":
        content = input("内容を入力してください。\n")
        chat.append({"role": "system", "content": content})

    print("会話をはじめます : q または quit で終了")
    print("--"*20)
    while True:
        user = input("<あなた>\n")
        if user == "q" or user == "quit":
            cost = calculate_cost(amount_tokens, PRICE_PER_TOKEN)
            print(f"この会話のトークンは{amount_tokens}, 料金は約{cost}$でした。")
            save_chat_log(conversation_name, chat)
            break
        else:
            chat.append({"role": "user", "content": user})

        print("<ChatGPT>")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=chat
        )
        msg = response["choices"][0]["message"]["content"].lstrip()
        amount_tokens += response["usage"]["total_tokens"]
        print(msg)
        chat.append({"role": "assistant", "content": msg})

if __name__ == "__main__":
    main()
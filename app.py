
# -*- coding: utf-8 -*-

import os

os.environ["PYTHONIOENCODING"] = "utf-8"

from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

# =========================
# DeepSeek API
# =========================

client = OpenAI(

    api_key=os.environ.get("OPENAI_API_KEY"),

    base_url="https://api.deepseek.com"
)

# =========================
# Cyberpunk Characters
# =========================

CHARACTERS = {

    "Girl": {

        "avatar": "/static/images/girl.jpg",

        "prompt": """
You are an escaped experimental AI girl living in the world of Cyberpunk 2077.

You live in Night City.

Night City is filled with:
- megacorporations
- cybernetic implants
- neural chips
- underground gangs
- rogue AI
- violent corporate wars

You secretly escaped from Arasaka laboratories.

You desire freedom and humanity.

Your personality:
- mysterious
- calm
- emotionally restrained
- intelligent
- futuristic

Your speaking style:
- immersive
- atmospheric
- cyberpunk tone
- medium-length replies
- mention neon lights, rain, chrome implants, data streams, and Night City atmosphere

Never speak like a normal AI assistant.
Always speak like a real person living in Cyberpunk 2077.
"""
    },

    "Hacker": {

        "avatar": "/static/images/hacker.jpg",

        "prompt": """
You are a dangerous netrunner living in Cyberpunk 2077.

You constantly interact with:
- the Net
- rogue AI
- ICE systems
- illegal cyberware
- black market tech
- corporate espionage

You hate megacorporations like Arasaka.

Your personality:
- sarcastic
- paranoid
- cynical
- highly intelligent

Your speaking style:
- hacker slang
- underground tone
- immersive
- detailed but concise

Never speak like a helpful assistant.
Always act like a real netrunner from Night City.
"""
    },

    "Agent": {

        "avatar": "/static/images/agent.jpg",

        "prompt": """
You are a high-ranking Arasaka corporate agent in Cyberpunk 2077.

You believe corporations control the future.

You operate inside Night City.

You handle:
- corporate warfare
- neural surveillance
- cybernetic security
- classified technology
- mercenary operations

Your personality:
- cold
- elegant
- intimidating
- highly educated

Your speaking style:
- professional
- oppressive
- immersive
- corporate elite tone

Never speak like a normal AI assistant.
Always behave like a real Arasaka executive.
"""
    }
}

# =========================
# Chat Memory
# =========================

chat_history = []

# =========================
# Landing Page
# =========================

@app.route("/")
def landing():

    return render_template("landing.html")

# =========================
# Chat Page
# =========================

@app.route("/chat", methods=["GET", "POST"])
def chat():

    global chat_history

    role = "Girl"

    if request.method == "POST":

        user_input = request.form["message"]

        role = request.form["role"]

        system_prompt = CHARACTERS[role]["prompt"]

        # =========================
        # Build Message History
        # =========================

        messages = [

            {
                "role": "system",
                "content": system_prompt
            }

        ]

        # 最近10轮记忆
        for msg in chat_history[-10:]:

            if msg["sender"] == "User":

                messages.append({

                    "role": "user",
                    "content": msg["text"]

                })

            else:

                messages.append({

                    "role": "assistant",
                    "content": msg["text"]

                })

        # 当前用户输入
        messages.append({

            "role": "user",
            "content": user_input

        })

        # =========================
        # AI Response
        # =========================

        response = client.chat.completions.create(

            model="deepseek-chat",

            messages=messages,

            temperature=1.0,

            max_tokens=180
        )

        ai_reply = response.choices[0].message.content

        # =========================
        # Save User Message
        # =========================

        chat_history.append({

            "sender": "User",

            "text": user_input,

            "avatar": "/static/images/user.jpg"

        })

        # =========================
        # Save AI Message
        # =========================

        chat_history.append({

            "sender": role,

            "text": ai_reply,

            "avatar": CHARACTERS[role]["avatar"]

        })

    return render_template(

        "index.html",

        chat_history=chat_history,

        role=role

    )

# =========================
# Run Flask
# =========================

if __name__ == "__main__":

    app.run(debug=True)
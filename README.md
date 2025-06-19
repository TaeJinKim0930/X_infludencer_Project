```markdown
# 🤖 X Autopilot Agent (Crypto Twitter Bot)

An AI-powered Twitter bot designed to act as a friendly yet credible crypto influencer.  
This bot automatically posts daily crypto market insights, replies to comments using GPT, and engages with related tweets — all in Korean, styled like a real human expert.

---

## ✨ Features

- ✅ Automatically posts daily market summary threads at peak times (12:00 and 18:00 KST)
- 💬 Listens for mentions and responds with GPT-generated, natural, humorous or empathetic replies (currently disabled by default)
- 📍 All interactions are in **Korean**, using a friendly and casual tone, ending with a disclaimer like:  
  _“투자는 각자 책임이니까~🤭” (Invest at your own risk!)_

---

## 📁 File Structure

```

x\_autopilot\_agent.py   # Main bot script
.env                   # Your API keys and credentials
install.sh             # Environment setup script (optional)

````

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-name/x-autopilot-agent.git
cd x-autopilot-agent
````

### 2. Create `.env` file with your API credentials

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Twitter OAuth1.0a
TW_API_KEY=your_twitter_api_key
TW_API_SECRET=your_twitter_api_secret
TW_ACCESS_TOKEN=your_access_token
TW_ACCESS_SECRET=your_access_secret

# Twitter OAuth2.0 (for bearer token retrieval, optional)
TW_CLIENT_ID=your_client_id
TW_CLIENT_SECRET=your_client_secret

# Optional: If you're using a manually issued bearer token instead of programmatic auth
TW_BEARER_TOKEN=your_bearer_token
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the bot

```bash
python x_autopilot_agent.py
```

---

## 🔑 Twitter/X Authentication

Due to recent policy changes by X (Twitter), the OAuth2.0 Client Credentials Flow may return a `403 Forbidden` even with valid client ID/secret.
To bypass this:

1. Manually generate a **Bearer Token** from the X Developer Portal.
2. Ensure the app permission is set to:

```
Read and write and Direct message
Read Posts and profile information, read and post Direct messages
```

3. Add the token to `.env` as `TW_BEARER_TOKEN` and it will be used directly.

---

## 🧠 What It Does

| Feature       | Description                                                       |
| ------------- | ----------------------------------------------------------------- |
| 🔁 Auto-post  | Posts crypto trend summary threads twice a day                    |
| 💬 Auto-reply | Responds to mentions with GPT-powered friendly comments           |
| 🤖 GPT styles | Randomizes between informative, empathetic, or humorous responses |
| ⏱ Scheduling  | Based on Korean time (Asia/Seoul)                                 |
| 📈 Growth     | Designed to grow followers and engagement organically             |

---

## 📢 Disclaimer

This bot is for educational and experimental use.
It includes investment-related commentary, but **investment decisions are your own responsibility**. Always end posts with:

> 투자는 각자 책임이니까\~🤭

---

## 📬 Questions?

Feel free to open an issue or fork the repo with improvements!
Designed with ❤️ for crypto + AI automation.

```

필요하면 위 내용을 한국어 버전으로도 바꿔드릴 수 있습니다. 혹시 프로젝트 공개 레포로 만들 계획이라면 badge, 라이선스, 배포 문구도 추가해드릴게요.
```

# X Autopilot Agent: GPT 기반 암호화폐 트위터 인플루언서 자동화
import openai
import tweepy
import time
import random
import pytz
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

# --- OpenAI API 키 설정 ---
OPENAI_API_KEY = "여기에_입력"

# --- X API 키 설정 ---
TW_API_KEY = os.getenv("TW_API_KEY")
TW_API_SECRET = os.getenv("TW_API_SECRET")
TW_ACCESS_TOKEN = os.getenv("TW_ACCESS_TOKEN")
TW_ACCESS_SECRET = os.getenv("TW_ACCESS_SECRET")

# --- 인증 ---
auth = tweepy.OAuth1UserHandler(TW_API_KEY, TW_API_SECRET, TW_ACCESS_TOKEN, TW_ACCESS_SECRET)
api = tweepy.API(auth)
openai.api_key = OPENAI_API_KEY

# --- 타임존 설정 ---
korea = pytz.timezone("Asia/Seoul")

# --- 프롬프트 스타일 (정보형, 공감형, 유머형) ---
def make_prompt_style(style, user_id, comment):
    if style == "info":
        context = "비트코인, 이더리움 등 암호화폐 시장의 흐름, 투자 마인드, 트렌드 해석 등 실질적인 도움을 줄 수 있는 관점으로 답변해줘."
    elif style == "empathy":
        context = "개인 투자자로서 느끼는 감정이나 공감을 우선해줘. 같이 힘내자는 말투도 좋아."
    else:
        context = "재미있고 드립 있는 말투로 답변해줘. 농담이나 트위터 밈도 적절히 활용해."

    return f"""
    [대화 배경]
    당신은 한국 트위터에서 활동하는 친근하지만 전문성을 갖춘 암호화폐 분석 전문가입니다.

    [요청 내용]
    아래는 한 유저가 내 트윗에 달아준 댓글입니다. 다음 조건을 만족하도록 답변해줘:

    - 트위터에 어울리는 길이 (짧고 임팩트 있게)
    - 한국어로 작성, 반말처럼 친근한 말투
    - 마지막 문장에 꼭 포함: "투자는 각자 책임이니까~🤭"
    - 해시태그나 이모지(🔥💸📉📈)는 선택적 삽입

    [상황]
    @{user_id}가 이렇게 댓글을 달았어:
    "{comment}"

    [답변 스타일 가이드]
    {context}
    """

# --- GPT 응답 생성 ---
def generate_gpt_reply(user_id, comment):
    style = random.choice(["info", "empathy", "humor"])
    prompt = make_prompt_style(style, user_id, comment)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "너는 코인 트위터 인플루언서로 활동하고 있어. 팔로워들과 친근하게 소통해."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content.strip()
        # CTA 유도 문장 추가
        cta = random.choice([
            "리트윗 하면 운 좋아질지도?💸",
            "비슷한 얘기 오늘 올렸어. 타임라인 구경 ㄱ",
            "정보 도움됐으면 팔로우도 부탁~🔥"
        ])
        return f"{reply}\n\n{cta}"
    except Exception as e:
        print("GPT 호출 오류:", e)
        return None

# --- 댓글 응답 처리 ---
REPLIED_IDS = set()

def reply_to_mentions():
    try:
        mentions = api.mentions_timeline(count=5)
        for mention in mentions:
            if mention.id in REPLIED_IDS:
                continue
            print(f"💬 댓글 발견: @{mention.user.screen_name}: {mention.text}")
            reply_text = generate_gpt_reply(mention.user.screen_name, mention.text)
            if reply_text:
                api.update_status(status=f"@{mention.user.screen_name} {reply_text}", in_reply_to_status_id=mention.id)
                REPLIED_IDS.add(mention.id)
                print("✅ GPT 답변 완료:", reply_text)
                time.sleep(random.randint(60, 180))
    except Exception as e:
        print("❌ 답변 중 오류:", e)

# --- 오늘의 코인 요약 스레드 자동 포스팅 ---
def post_daily_thread():
    today = datetime.now(korea).strftime("%Y년 %m월 %d일")
    binanceLink = "https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00VKZPQ0DA"
    binanceCode = "CPA_00VKZPQ0DA"
    prompt = f"""
    오늘 날짜는 {today}이야. 비트코인, 이더리움 등 주요 암호화폐의 트렌드, 가격 동향, 시장 이슈를 요약해서 **한글 트위터 스레드 형식으로** 작성해줘.

    조건은 다음과 같아:

    1. 각 트윗은 250자 내외로.
    2. 총 3~5개의 트윗으로 구성할 것.
    3. 말투는 친근하고 자연스럽게.
    4. 마지막 트윗에는 반드시 아래 2가지 항목을 포함할 것:
    - 문구: "투자는 각자 책임이니까~🤭"
    - 내 바이낸스 레퍼럴 링크와 코드:
        - 링크: {binanceLink}
        - 코드: {binanceCode}

    절대 이 마지막 두 항목을 빠뜨리지 말고 항상 포함해줘!
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "암호화폐 시장 분석을 요약해서 트위터용 스레드로 작성해줘."},
                {"role": "user", "content": prompt}
            ]
        )
        thread = response.choices[0].message.content.strip().split("\n\n")
        tweet_id = None
        for i, tweet in enumerate(thread):
            if i == 0:
                post = api.update_status(tweet)
                tweet_id = post.id
            else:
                post = api.update_status(tweet, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
                tweet_id = post.id
            time.sleep(5)
        print("📌 오늘의 코인 스레드 완료")
    except Exception as e:
        print("❌ 스레드 작성 오류:", e)

# --- 실행 루프 ---
if __name__ == "__main__":
    while True:
        now = datetime.now(korea)
        if now.hour == 12 or now.hour == 18:  # 점심 & 퇴근 시간대 업로드
            post_daily_thread()
        reply_to_mentions()
        time.sleep(600)  # 10분 간격 실행
#!/bin/bash

echo "✅ Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✅ Installing required libraries..."
pip install --upgrade pip
pip install openai tweepy python-dotenv pytz

echo "✅ Creating .env template file..."
cat <<EOT > .envz
OPENAI_API_KEY=your_openai_key_here
TW_API_KEY=your_twitter_api_key
TW_API_SECRET=your_twitter_api_secret
TW_ACCESS_TOKEN=your_twitter_access_token
TW_ACCESS_SECRET=your_twitter_access_secret
EOT

echo "📌 .env file has been created. Please fill in your API credentials."
echo "▶ To run the bot: source venv/bin/activate && python your_script_name.py"

# Cyria: The Financial Advisor AI Bot Documentation

Welcome to the comprehensive guide for Cyria, your AI-powered financial advisor bot! This document provides a detailed overview of the bot's functionality, setup, and use cases, along with instructions for installation and customization.

---

## 1. Introduction

### What Is Cyria?
Cyria is an intelligent Twitter bot designed to provide financial advice and engage with users on topics related to finance. Leveraging advanced AI algorithms, Cyria can respond to user queries, share insightful financial tips, and maintain meaningful interactions on Twitter.

### Key Features
- **AI-Powered Financial Advice**: Delivers accurate and relevant financial advice tailored to user queries.
- **Automated Tweet Posting**: Shares financial tips, market updates, and general advice at scheduled intervals.
- **Engagement Tracking**: Keeps logs of replied mentions to avoid redundancy in responses.
- **Customizable Templates**: Includes pre-designed templates for financial advice tweets, which can be personalized.
- **Deployment Ready**: Supports deployment on platforms like Heroku using a `Procfile` for process management.

### Use Cases
- **Financial Education**: Provide quick, reliable advice on budgeting, investments, and financial planning.
- **Market Updates**: Share real-time financial news or updates to keep followers informed.
- **Customer Support**: Address frequently asked questions about finance-related topics.
- **Community Engagement**: Foster an active online presence by interacting with followers and building trust.

---

## 2. How It Works

### Core Functionality
1. **Listening for Mentions**:
   - Cyria continuously monitors your Twitter account for mentions and financial-related queries.
   - It ensures no duplicate responses by checking `replied_mentions.txt`.
2. **Providing Financial Advice**:
   - The `content_generator.py` script uses AI to generate contextually accurate financial advice or information.
3. **Posting Financial Tips**:
   - Cyria regularly posts financial tips or market insights, either scheduled or dynamically generated.
4. **Logging Activity**:
   - All interactions, including tweets and replies, are logged in `bot.log` for review and troubleshooting.

### Components
- **`main.py`**:
   - The core script managing all operations, including Twitter API interactions, advice generation, and logging.
- **`content_generator.py`**:
   - Focused on creating financial advice content using predefined models or custom logic.
- **Utilities (`utils`)**:
   - Provides auxiliary functions for text processing and API requests.
- **Templates**:
   - Stores pre-written financial advice messages for customization.

---

## 3. Installation and Setup

### Prerequisites
- **Python 3.8+**
- **Twitter Developer Account**: Obtain API keys and tokens.
- **Heroku CLI (Optional)**: For deployment.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies**:
   Install the required Python libraries using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file with the following keys:
   ```env
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET_KEY=your_api_secret_key
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
   ```

4. **Run Cyria**:
   Execute the main script to start the bot:
   ```bash
   python main.py
   ```

5. **Deploy on Heroku (Optional)**:
   - Create a new Heroku app.
   - Push the repository and set environment variables in Heroku.
   - Use the `Procfile` to manage processes.

---

## 4. Customizing Cyria

### Modifying Templates
- Navigate to the `templates` folder.
- Edit or add new financial advice templates for tweets.
- Ensure consistency in tone and formatting.

### Extending Functionality
- Introduce new scripts or functions in `utils` or other modules.
- Update `main.py` to incorporate the added features.
- Test thoroughly before deployment.

### Adjusting Reply Logic
- Update the logic in `replied_mentions.txt` handling within `main.py` to change how interactions are tracked.

---

## 5. Code Overview

### `main.py`
- Serves as the orchestrator for Cyria’s operations.
- Key sections:
  - **Initialization**: Configures API connections and loads environment variables.
  - **Main Loop**: Monitors Twitter for mentions and triggers content generation or tweets.

### `content_generator.py`
- Generates financial advice based on user queries or predefined scenarios.
- Uses AI models or logic for dynamic content creation.

### `utils`
- Includes helper functions for:
  - Parsing and formatting financial-related text.
  - Handling API responses and file management.

### `templates`
- Contains pre-written financial advice and tips.
- Easily customizable to align with specific themes or requirements.

---

## 6. Logging and Monitoring

### Interpreting `bot.log`
- **Purpose**: Provides a detailed log of Cyria’s actions for debugging and performance tracking.
- **Format**:
  - Timestamps for each activity.
  - Details of mentions replied to and tweets posted.

### Managing `replied_mentions.txt`
- Tracks mentions already addressed to prevent redundant responses.
- Each line corresponds to a tweet ID.
- Regularly review or reset the file if needed.

---

## 7. Troubleshooting

### Common Issues
1. **Authentication Errors**:
   - Verify the accuracy of API keys in `.env`.
   - Check for exceeded rate limits in the Twitter Developer Dashboard.

2. **No Replies to Mentions**:
   - Review the logic in `main.py`.
   - Ensure `replied_mentions.txt` is being updated correctly.

3. **Deployment Problems**:
   - Validate `Procfile` syntax.
   - Inspect Heroku logs for error messages.

### Debugging Tips
- Enable detailed logging in `bot.log` for better insights.
- Test individual modules (e.g., `content_generator.py`) to isolate issues.

---

## 8. FAQ

### Q: Can Cyria handle multiple Twitter accounts?
A: Yes, but each account requires its own set of API credentials.

### Q: How does Cyria ensure compliance with Twitter’s policies?
A: Cyria adheres to Twitter’s automation guidelines, avoiding spam and focusing on meaningful interactions.

### Q: Can Cyria schedule tweets?
A: Absolutely. Incorporate scheduling libraries like `schedule` into `main.py`.

### Q: Does Cyria support sentiment analysis?
A: Yes, by integrating sentiment analysis libraries within `content_generator.py`.

---

## 9. Future Enhancements
- **Advanced AI Models**: Use more sophisticated models for nuanced financial advice.
- **Interactive Dashboards**: Provide a web interface for monitoring and controlling Cyria’s activity.
- **Multilingual Support**: Expand to deliver financial advice in various languages.
- **Real-Time Notifications**: Add live alerts for critical financial updates.

---

## 10. Conclusion
Cyria is a powerful AI-driven financial advisor bot designed to enhance user engagement and provide actionable financial advice on Twitter. With its customizable templates, automated interactions, and intelligent content generation, Cyria is an invaluable tool for individuals and organizations aiming to make an impact in the financial space. By following this guide, you can fully utilize Cyria’s potential and even expand its capabilities to suit evolving needs.


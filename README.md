# xMatters Performance data Chatbot

This project is to use langchain agent along with OpenAI api Function calling to allow for chatting with xMatters Incident/User/Group performance data.

## Features

- You can ask natural language questions about xMatters performance metrics, users and groups, such as "What is the performance of the group "Subgroup Nick" in the past year?" or "Who is the supervisor of group Subgroup Nick?"

## Installation

To install this project, you need to have the following prerequisites:

- Python 3.10.10 or higher
- pip
- OpenAI API key
- xMatters API key

Then, you can clone this repository and run the following commands:

```bash
cd xMatters-chatbot
pip install -r requirements.txt
python main.py
```

Then copy .env_template to .env, filling in the required values.

## Usage

To use this project, you need to launch the main.py script and open the web interface in your browser.
Then, you can start chatting with the chatbot by typing or speaking your questions.

```
User: What is the performance of my group "Subgroup Nick" in the past year?

> Entering new  chain...

Invoking: `get_group_performance` with `{'group_id': 'Subgroup Nick', 'start_time_utc': '2022-07-10T00:00:00Z', 'end_time_utc': '2023-07-10T00:00:00Z'}`


{'duration': '445', 'total': 1, 'data': [{'alerts': {'total': 58, 'escalations': {'total': 0, 'peers': 0, 'notSpecified': 0, 'managers': 0}, 'timeToFirstResponse': {'max': 1752407, 'mean': 211273}, 'delivered': 58, 'failed': 0, 'responseContribution': {'negative': 3, 'neutral': 1, 'positive': 24, 'notSpecified': 0}, 'noResponse': 30, 'totalResponded': 28}, 'recipient': {'firstName': 'Nick', 'lastName': 'Pirson', 'targetName': 'npirson', 'id': '5c1ca07e-bbba-4ad1-8ee6-66448f60ea52', 'type': 'PERSON'}}], 'count': 1, 'links': {'self': '/api/abe/1/performance/GROUPS?sortBy=alerts.total&sortOrder=DESCENDING&from=2022-07-10T00:00:00Z&to=2023-07-10T00:00:00Z&limit=100&offset=0&offset=0&supervisedByMe=false&parentGroup=86e663d1-8a73-49b6-8046-5aed31214237'}}The performance of your group "Subgroup Nick" in the past year is as follows:

- Total alerts: 58
- Delivered alerts: 58
- Failed alerts: 0
- Time to first response (mean): 211,273 milliseconds
- No response: 30
- Total responded: 28
- Response contribution: 
  - Positive: 24
  - Negative: 3
  - Neutral: 1

Please let me know if you need any further information.

> Finished chain.
```

## License

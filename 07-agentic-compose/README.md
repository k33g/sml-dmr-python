Start the bot:
```bash
docker compose up --build --no-log-prefix -d
```

Connect to the bot:
```bash
docker exec -it $(docker compose ps -q small-bot) /bin/bash
# or
docker exec -it 07-agentic-compose-small-bot-1 /bin/bash
```

Start the conversation:
```bash
python main.py
```
# ETS2 Convoy Server - Discord Integration

## Description

This project adds Discord integration to ETS2 convoy server, automatically sending notifications about player connections and disconnections.

## Features

- ✅ Real-time ETS2 server log monitoring
- ✅ Automatic Discord notifications for player connections
- ✅ Automatic Discord notifications for player disconnections
- ✅ Current connected players counter
- ✅ Automatic detection of server maximum slots
- ✅ Configurable icons and texts
- ✅ Avoiding duplicates and old notifications
- ✅ Running as separate Docker container
- ✅ Universal monitor - can monitor different servers (ETS2/ATS)

## Configuration

### 1. Discord Webhook

1. Create a webhook on your Discord server:
   - Go to channel settings → Integrations → Webhooks
   - Click "New Webhook"
   - Copy the webhook URL

2. Add URL to `.env` file:
```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url_here
```

### 2. Message formatting configuration

In `.env` file you can customize notification format:

```bash
# Icons (emoji or other characters)
DISCORD_CONNECT_ICON=🚛          # Icon for connections
DISCORD_DISCONNECT_ICON=🔴       # Icon for disconnections

# Texts
DISCORD_CONNECT_TEXT=connected    # Text for connections
DISCORD_DISCONNECT_TEXT=disconnected  # Text for disconnections

# Container name to monitor (ets2-server or ats-server)
MONITOR_CONTAINER_NAME=ets2-server
```

### 3. Message format

Messages are sent in simple single-line format with current player counter:
```
🚛 **PlayerName** connected (1/8)
🔴 **PlayerName** disconnected (0/8)
```

Where:
- First number is current connected players count
- Second number is maximum server slots (detected automatically)

## Running

### Starting the entire service

```bash
docker compose up -d
```

This will start both:
- ETS2 convoy server (`ets2-server`)
- Discord monitor (`discord-monitor`)

### Starting only the monitor (if server is already running)

```bash
docker compose up discord-monitor -d
```

### Checking monitor logs

```bash
docker logs ets2-discord-monitor -f
```

## Advanced Configuration

### Switching between ETS2 and ATS servers

To monitor ATS server instead of ETS2:

1. Change in `.env`:
```bash
MONITOR_CONTAINER_NAME=ats-server
```

2. Restart monitor:
```bash
docker compose restart discord-monitor
```

### Message Examples

Connection:
```
🚛 **Kaceusz** connected (1/8)
```

Disconnection:
```
🔴 **PlayerName** disconnected (0/8)
```

### Custom Icons and Texts

You can customize icons and texts for different languages:

```bash
# For Polish
DISCORD_CONNECT_ICON=🚛
DISCORD_CONNECT_TEXT=połączony
DISCORD_DISCONNECT_ICON=🔴
DISCORD_DISCONNECT_TEXT=rozłączony

# For German
DISCORD_CONNECT_ICON=🚛
DISCORD_CONNECT_TEXT=verbunden
DISCORD_DISCONNECT_ICON=🔴
DISCORD_DISCONNECT_TEXT=getrennt

# For French
DISCORD_CONNECT_ICON=🚛
DISCORD_CONNECT_TEXT=connecté
DISCORD_DISCONNECT_ICON=🔴
DISCORD_DISCONNECT_TEXT=déconnecté
```

## Troubleshooting

### Problem: Monitor doesn't see logs

1. Check if server container is running:
```bash
docker ps | grep ets2
```

2. Check container name in `.env`:
```bash
cat .env | grep MONITOR_CONTAINER_NAME
```

3. Check if container name matches:
```bash
docker logs ets2-discord-monitor
```

### Problem: Webhook doesn't work

1. Check if URL is correct in `.env`
2. Check if webhook exists on Discord server
3. Check monitor logs for errors:
```bash
docker logs ets2-discord-monitor -f
```

### Problem: Duplicate notifications

The monitor has built-in deduplication:
- Uses only MP session logs (not chat)
- Tracks already sent notifications
- Filters old logs from startup

## Technical Details

### Log Patterns

The monitor searches for these patterns in ETS2 server logs:

**Player connection:**
```
[MP] PlayerName connected, client_id = X
```

**Player disconnection:**
```
[MP] PlayerName disconnected
```

**Maximum players:**
```
[MP] Maximum number of players: X
```

### Files

- `discord_notifier/log_monitor.py` - Main monitoring script
- `Dockerfile.monitor` - Docker image for monitor
- `docker-compose.yml` - Service definition
- `.env` - Configuration

### Dependencies

- Python 3.11
- requests library
- Docker API access
- ETS2/ATS dedicated server

## File Structure

```
.
├── docker-compose.yml           # Container configuration
├── Dockerfile.monitor          # Dockerfile for Discord monitor
├── .env                        # Environment variables
└── discord_notifier/
    └── log_monitor.py          # Main monitor script
```

## Technologies

- **Python 3.11** - monitor script language
- **Docker & Docker Compose** - containerization
- **Discord Webhooks** - Discord integration
- **ETS2 Dedicated Server** - game server

## Example Notifications

When player connects:
```
🚛 **Kaceusz** connected (1/8)
```

When player disconnects:
```
🔴 **Kaceusz** disconnected (0/8)
```

Numbers in brackets mean: (current number of players)/(maximum number of slots)

## Security

- Webhook URL is stored in environment variables
- Monitor has read-only access to Docker logs
- No storage of players' personal data

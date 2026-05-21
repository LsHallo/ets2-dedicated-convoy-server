#!/usr/bin/env python3
"""
ETS2 Convoy Server - Discord Log Monitor
Monitors server logs and sends Discord notifications about player connections/disconnections
"""

import re
import time
import subprocess
import json
import requests
import os
from datetime import datetime
from typing import Optional

class ETS2LogMonitor:
    def __init__(self, webhook_url: str, container_name: str = "ets2-server"):
        self.webhook_url = webhook_url
        self.container_name = container_name
        self.last_position = 0
        
        # Player counters
        self.current_players = 0
        self.max_players = 8  # default value
        self.max_players_found = False  # flag to track if max players was already found and logged
        
        # Message configuration from environment variables
        self.connect_icon = os.getenv('DISCORD_CONNECT_ICON', '🚛')
        self.disconnect_icon = os.getenv('DISCORD_DISCONNECT_ICON', '🔴')
        self.connect_text = os.getenv('DISCORD_CONNECT_TEXT', 'connected')
        self.disconnect_text = os.getenv('DISCORD_DISCONNECT_TEXT', 'disconnected')
        
        # Regex patterns for connection logs - using only lines with client_id
        self.connect_pattern = re.compile(r'\[MP\] (\w+) connected, client_id = (\d+)')
        self.disconnect_pattern = re.compile(r'\[MP\] (\w+) disconnected, client_id = (\d+)')
        
        # Pattern for maximum number of players
        self.max_players_pattern = re.compile(r'\[MP\] Maximum number of players: (\d+)')
        
        # Ignoring lines with [Chat] to avoid duplicates
        
    def get_logs(self) -> str:
        """Retrieves latest logs from Docker container"""
        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", "50", self.container_name],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving logs: {e}", flush=True)
            return ""
    
    def send_discord_notification(self, player_name: str, action: str, client_id: str):
        """Sends notification to Discord webhook"""
        
        # Choose icon and text based on action
        if action == "connected":
            icon = self.connect_icon
            action_text = self.connect_text
        else:
            icon = self.disconnect_icon
            action_text = self.disconnect_text
        
        # Create simple single-line message with player counter
        message = f"{icon} **{player_name}** {action_text} ({self.current_players}/{self.max_players})"
        
        payload = {
            "content": message
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            print(f"✅ Discord notification sent: {player_name} {action}", flush=True)
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending Discord notification: {e}", flush=True)
    
    def process_log_line(self, line: str):
        """Processes single log line"""
        
        # Ignore [Chat] lines to avoid duplicates
        if '[Chat]' in line:
            return
        
        # Check maximum number of players (only log once)
        max_players_match = self.max_players_pattern.search(line)
        if max_players_match:
            new_max_players = int(max_players_match.group(1))
            if not self.max_players_found or new_max_players != self.max_players:
                self.max_players = new_max_players
                self.max_players_found = True
                print(f"📊 Maximum number of players: {self.max_players}", flush=True)
            return
        
        # Check player connection
        connect_match = self.connect_pattern.search(line)
        if connect_match:
            player_name = connect_match.group(1)
            client_id = connect_match.group(2)
            self.current_players += 1
            print(f"👥 Players online: {self.current_players}/{self.max_players}", flush=True)
            self.send_discord_notification(player_name, "connected", client_id)
            return
        
        # Check player disconnection
        disconnect_match = self.disconnect_pattern.search(line)
        if disconnect_match:
            player_name = disconnect_match.group(1)
            client_id = disconnect_match.group(2)
            self.current_players -= 1
            if self.current_players < 0:  # protection against negative value
                self.current_players = 0
            print(f"👥 Players online: {self.current_players}/{self.max_players}", flush=True)
            self.send_discord_notification(player_name, "disconnected", client_id)
            return
    
    def monitor_logs(self, interval: int = 5):
        """Main log monitoring loop"""
        print(f"🔍 Starting log monitoring for container '{self.container_name}'...", flush=True)
        print(f"📡 Discord webhook configured", flush=True)
        print(f"⏱️  Checking every {interval} seconds", flush=True)
        print("=" * 60, flush=True)
        
        # Initialization - get current logs to avoid notifications about old events
        print("🔄 Initialization - retrieving current logs...", flush=True)
        initial_logs = self.get_logs()
        processed_logs = set()
        
        if initial_logs:
            initial_lines = initial_logs.split('\n')
            
            # Find maximum number of players from logs
            for line in initial_lines:
                max_players_match = self.max_players_pattern.search(line)
                if max_players_match:
                    self.max_players = int(max_players_match.group(1))
                    self.max_players_found = True
            
            # Count current number of players based on historical logs
            connected_players = set()
            for line in initial_lines:
                connect_match = self.connect_pattern.search(line)
                if connect_match:
                    player_name = connect_match.group(1)
                    client_id = connect_match.group(2)
                    connected_players.add(client_id)
                    
                disconnect_match = self.disconnect_pattern.search(line)
                if disconnect_match:
                    client_id = disconnect_match.group(2)
                    connected_players.discard(client_id)
                    
                # Add to processed logs to avoid duplicates
                if '[MP]' in line and ('connected' in line or 'disconnected' in line):
                    if 'client_id' in line:
                        line_hash = hash(line.strip())
                        processed_logs.add(line_hash)
            
            self.current_players = len(connected_players)
            print(f"📊 Maximum number of players: {self.max_players}", flush=True)
            print(f"👥 Current number of players: {self.current_players}", flush=True)
            print(f"✅ Ignored {len(processed_logs)} old connection/disconnection events", flush=True)
        
        print("🚀 Monitor ready! Monitoring new events...", flush=True)
        
        while True:
            try:
                logs = self.get_logs()
                
                if logs:
                    lines = logs.split('\n')
                    
                    for line in lines:
                        # Check if line contains connection/disconnection info or max players
                        if '[MP]' in line:
                            # Check max players
                            if 'Maximum number of players:' in line:
                                self.process_log_line(line)
                                continue
                                
                            # Check connections/disconnections - ignore [Chat] lines
                            if ('connected' in line or 'disconnected' in line) and 'client_id' in line:
                                # Use unique line identifier to avoid duplicates
                                line_hash = hash(line.strip())
                                
                                if line_hash not in processed_logs:
                                    processed_logs.add(line_hash)
                                    self.process_log_line(line)
                                    
                                    # Limit size of processed logs set
                                    if len(processed_logs) > 1000:
                                        # Keep only newest 500 logs
                                        processed_logs = set(list(processed_logs)[-500:])
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping log monitor...", flush=True)
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}", flush=True)
                time.sleep(interval)

def main():
    # Read webhook URL from environment variable
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ Error: Missing DISCORD_WEBHOOK_URL in environment variables")
        print("Set environment variable: export DISCORD_WEBHOOK_URL='your_webhook_url'")
        return 1
    
    # Read container name to monitor
    container_name = os.getenv('MONITOR_CONTAINER_NAME', 'ets2-server')
    
    # Check if Docker container is running
    try:
        subprocess.run(
            ["docker", "inspect", container_name],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"❌ Error: Container '{container_name}' is not running")
        print(f"Start server with command: docker compose up {container_name} -d")
        return 1
    
    # Create and run monitor
    monitor = ETS2LogMonitor(webhook_url, container_name)
    monitor.monitor_logs()
    
    return 0

if __name__ == "__main__":
    exit(main())

#!/bin/bash

echo "Starting dhcpcd service..."
sudo systemctl start dhcpcd

echo "Starting hostapd service..."
sudo systemctl start hostapd

sudo systemctl restart hostapd
sudo systemctl restart dhcpcd

echo "Checking status of hostapd..."
HOSTAPD_STATUS=$(sudo systemctl status hostapd | grep -i "active (running)")

if [[ -z "$HOSTAPD_STATUS" ]]; then
    echo "Error: hostapd service failed to start." | tee -a /var/log/startup_errors.log
    exit 1
else
    echo "hostapd is running successfully."
fi

echo "Log files process"
LOG_DIR="/home/integralsenso/Desktop/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/log_$(date '+%Y-%m-%d_%H-%M-%S').log"
echo "Log file created: $LOG_FILE"

echo "Starting Flask API without logs..."
sudo sudo /usr/bin/python3 "/home/integralsenso/Desktop/repo/PillowWebsite/WebSite/runGame.py" &
API_PID=$!
echo "Flask API started with PID: $API_PID"

while true; do
    sleep 60
done

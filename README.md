# Serial Log Capture Utility Program

Python script to capture serial log and log in a file

### Find Raspberry Pi in your network using nmap

```bash
sudo nmap -sT --min-parallelism 100 -O 192.168.1.0/24
```

### Enable and Start the Service

1. Copy service file to systemd
   ```bash
   sudo cp serial_log_capture.service /etc/systemd/system
   ```
2. Reload the systemd manager configuration:
   ```bash
   sudo systemctl daemon-reload
   ```

3. Enable the service to start on boot:

   ```bash
   sudo systemctl enable serial_log_capture.service
   ```
4. Start the service immediately:

   ```bash
   sudo systemctl start serial_log_capture.service
   ```

### Check the Status of the Service

You can check if your service is running with:

```bash
sudo systemctl status serial_log_capture.service
```

This setup ensures that your Python script at /path/app.py will start on system boot and automatically restart if it crashes.

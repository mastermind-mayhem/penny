#!/usr/bin/env bash
# ==============================================================================
# PENNY INSTALLATION SCRIPT
# ==============================================================================
set -e

REPO_URL="$https://github.com/mastermind-mayhem/penny.git}"
APP_NAME="penny"
INSTALL_DIR="/opt/${APP_NAME}"
VENV_DIR="${INSTALL_DIR}/venv"
BIN_DIR="/usr/local/bin"

# Root Check
if [ "$EUID" -ne 0 ]; then
  echo "[ERROR] Please run this script with sudo or as root."
  exit 1
fi

echo "==> Installing Python and pip..."
if ! command -v python3 &> /dev/null; then
    apt-get update
    apt-get install -y python3
fi

if ! command -v pip3 &> /dev/null; then
    apt-get install -y python3-pip
fi

echo "==> Installing Git..."
if ! command -v git &> /dev/null; then
    apt-get install -y git
fi

echo "==> Cloning repository..."
if [ -d "${INSTALL_DIR}" ]; then
    echo "[WARNING] Directory ${INSTALL_DIR} already exists. Removing it..."
    rm -rf "${INSTALL_DIR}"
fi

git clone "${REPO_URL}" "${INSTALL_DIR}"

echo "==> Setting up Python virtual environment..."
python3 -m venv "${VENV_DIR}"
${VENV_DIR}/bin/pip install --upgrade pip

if [ -f "${INSTALL_DIR}/requirements.txt" ]; then
    ${VENV_DIR}/bin/pip install -r "${INSTALL_DIR}/requirements.txt"
fi

echo "==> Creating systemd service..."

SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"

cat <<EOF > "${SERVICE_FILE}"
[Unit]
Description=${APP_NAME} Service
After=network.target

[Service]
ExecStart=${VENV_DIR}/bin/python ${INSTALL_DIR}/src/use.py
WorkingDirectory=${INSTALL_DIR}
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF

echo "==> Configuring activation time for the service..."

read -p "Enter the time of day to activate the service (HH:MM, 24-hour format): " ACTIVATION_TIME

TIMER_FILE="/etc/systemd/system/${APP_NAME}.timer"

cat <<EOF > "${TIMER_FILE}"
[Unit]
Description=Timer for ${APP_NAME} Service

[Timer]
OnCalendar=*-*-* ${ACTIVATION_TIME}
Persistent=true

[Install]
WantedBy=timers.target
EOF

echo "==> Reloading systemd daemon and enabling service..."
systemctl daemon-reload
systemctl enable ${APP_NAME}.service
systemctl start ${APP_NAME}.service

echo "==> Enabling and starting the timer..."
systemctl enable ${APP_NAME}.timer
systemctl start ${APP_NAME}.timer

echo "==> Service ${APP_NAME} has been created and started."

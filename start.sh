#!/bin/bash

COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

check_and_create_env() {
    if [ ! -f "$ENV_FILE" ]; then
        echo "Создание .env файла..."
        cat <<EOF >$ENV_FILE
#-------------------------Base-----------------------------------------------
PYTHON_VERSION=3.11.3
#--------------------------Data Base-----------------------------------------
DB_PORT=5432
DB_NAME=best_backend
DB_USER=postgres
DB_PASSWORD=best_backend
DB_HOST=postgres
#-----------------------Compose-----------------------------------------------
OUT_POSTGRES_PORT=5432
DEBUG_MODE_PORT_BACK=1939
DEBUG_MODE=False
BACKEND_PORT=777
EOF
        echo ".env файл создан."
    else
        echo ".env файл уже существует."
    fi
}

create_and_activate_venv() {
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        echo "Virtual environment created."
    else
        echo "Virtual environment already exists."
    fi

    echo "Activating virtual environment..."
    if [[ "$(uname -s)" == *"MINGW"* || "$(uname -s)" == *"CYGWIN"* ]]; then
        # For Windows
        source venv/Scripts/activate
    else
        # For Unix
        source venv/bin/activate
    fi
    echo "Virtual environment activated."
}

install_dependencies() {
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies from requirements.txt..."
        pip install -r requirements.txt
        echo "Dependencies installed."
    else
        echo "Error: requirements.txt not found."
    fi
}

start_uvicorn_server() {
    create_and_activate_venv
    echo "Starting uvicorn server..."
    uvicorn backend.app.api.main:app --host 0.0.0.0 --port 8080 & 
    uvicorn_pid=$!
    echo "Uvicorn server started on port 8080. Process ID: $uvicorn_pid"
}

start_yarn_server() {
    echo "Starting Yarn server..."
    if [ ! -d "quickstarts-historical-prices-api" ]; then
        echo "Error: Directory 'quickstarts-historical-prices-api' not found."
        return
    fi
    cd quickstarts-historical-prices-api
    yarn install
    yarn build
    yarn start
    cd -
    echo "Yarn server started."
}

start_both_servers() {
    start_uvicorn_server 
    echo "Press Enter to start the Yarn server..."
    read 
    start_yarn_server 
}

show_menu() {
    clear
    echo ""
    echo "==============================="
    echo "        The best backend       "
    echo "==============================="
    echo "1. Start Uvicorn Server"
    echo "2. Start Yarn Server"
    echo "3. Create and Activate Virtual Environment"
    echo "4. Start both servers"
    echo "9. Exit"
    echo
}

while true; do
    show_menu
    read -n 1 -p "Enter your choice [1-4]: " choice
    echo ""
    case $choice in
        1)
            start_uvicorn_server
            ;;
        2)
            start_yarn_server
            ;;
        3)  
            check_and_create_env
            create_and_activate_venv
            install_dependencies
            ;;
        4)
            start_both_servers
            ;;
        9)
            echo "Exit"
            break
            ;;
        *)
            echo "Wrong input. Choose between 1, 2, 3, and 4, please."
            ;;
        esac
    echo
done

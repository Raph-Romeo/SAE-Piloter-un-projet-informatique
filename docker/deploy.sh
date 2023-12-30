if ! command -v docker &> /dev/null
then
    echo "Docker n'est pas installé. Installation en cours..."

    if command -v apt-get &> /dev/null
    then
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    else
        echo "Système d'exploitation non pris en charge. Veuillez installer Docker manuellement."
        exit 1
    fi
fi

if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose n'est pas installé. Installation en cours..."
    sudo apt-get install -y docker-compose
fi

docker-compose down
docker network prune -f

docker build -t task_master_pro_backend ../backend_server

docker-compose up 


echo "Le déploiement est terminé."

Завантаження Python на сервер:

--------------------------------------------------------

sudo apt update

sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

wget https://www.python.org/ftp/python/3.9.8/Python-3.9.8.tgz

tar -xf Python-3.9.8.tgz

cd Python-3.9.8

./configure --enable-optimizations

make # ~15 хв

sudo make altinstall

cd /home

/home# python3.9 -V

python3.9 -m pip install --upgrade pip

pip install virtualenv

sudo apt install -y libxss1 libappindicator1 libindicator7

Дальше переходимо до розпакування архіву:

Для цього створюємо папку {name} у /home (/home/{name})

cd /home/{name}

-------------------------------------------------------------

Вивантажуємо архів проєкту через FileZilla

--------------------------------------------------------------

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

Для тестового запуску - python main.py

--------------------------------------------------------------

Якщо все працює - переходимо до запуску боту 24/7 (потрібен рут доступ)

--------------------------------------------------------------

nano /lib/systemd/system/{name}.service

Вставляємо:

[Unit] Description={name} bot After=network.target

[Service] EnvironmentFile=/etc/environment ExecStart=/home/{name}/venv/bin/python main.py ExecReload=/home/{name}/venv/bin/python main.py WorkingDirectory=/home/{name}/ KillMode=process Restart=always RestartSec=5

[Install] WantedBy=multi-user.target

---------------------------------------------------------------

systemctl enable {name} - активація 
systemctl start {name} - старт 
systemctl stop {name} - стоп 
systemctl restart {name} - перезапуск


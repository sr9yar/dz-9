# dz-9



## Installation

```

source venv/bin/activate
pip install -r requirements.txt

```


## Start

```

python scapy_sniffs_traffic.py
python scapy_gruyere.py
python xss_scan.py

```




## Scripts 


### Перехват трафика
```
python scapy_sniffs_traffic.py
```


### Запрос к gruyere
```
python scapy_gruyere.py
```


### Сканирование и проверка уязвимостей
```
python xss_scan.py
```


### Запрос к gruyere, содержащий уязвимость
```
python request_with_xss.py
```




## Initial project setup 

```

python -m venv ./venv

pip install scapy
pip install requests
pip install beautifulsoup4
pip install playwright
pip freeze > requirements.txt

playwright install

```




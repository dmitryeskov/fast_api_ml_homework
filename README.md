# FastAPI приложение классификаций с помощью ML-модели
API-сервис, с помощью которого можно классифицировать набор входящих признаков


## 1. Склонируйте и перейдите в репозиторий:
```
git clone https://github.com/dmitryeskov/fast_api_ml_homework.git
```
## 2. Установите необходимые зависимости
```
pip install -r requirements.txt
```

## 3. Установите ключ доступа
Это можно сделать либо изменение файла .env либо сгенерировать новые значения для ключа
Можно воспользоваться make
```
make secret
```
После этого SECRET_KEY в .env изменится

## 4. Заполните базу данных db.json
База данных по умолчанию, содержит запись для "otus"

Пароль сохраняется в виде хэша пароля "otus1234"

## 5. Модели
В папке models содержатся обученные модели для приложения

По умолчанию используется встроенная scikit-learn модель Wine, которая определяет класс вина по 13-ти входящим признакам

Признаки - числа float

Класс вина - числа int [0, 1, 2]

```
[
    "alcohol",                          # Содержание алкоголя (%)
    "malic_acid",                       # Яблочная кислота
    "ash",                              # Зола
    "alcalinity_of_ash",                # Щелочность золы
    "magnesium",                        # Магний (мг/100мл)
    "total_phenols",                    # Общее содержание фенолов
    "flavanoids",                       # Флавоноиды
    "nonflavanoid_phenols",             # Нефлавоноидные фенолы
    "proanthocyanins",                  # Проантоцианины
    "color_intensity",                  # Интенсивность цвета
    "hue",                              # Оттенок
    "od280/od315_of_diluted_wines",     # Поглощение при 280 нм / 315 нм
    "proline"                           # Пролин (мг/дл)
]
```

## 6. Обучение модели
Файлы для переобучения модели или создания новых хранятся в пакете utils

Можно использовать и обучить другую модель. Обученные модели должны сохраняться в models

Для обучения модели используйте utils

Например, для существующей модели models/wine_model.pkl выполнялся следующий скрипт
```
python3 -m utils.train_model_wine 
```



## 7. Использование

### 7.1 Пример авторизации
В начале работы необходимо авторизоваться, для этого вы можете получить токен, отправив следующий POST-запрос по маршруту `/token`:
```
curl --location 'http://localhost:8000/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=otus' \
--data-urlencode 'password=otus1234'
```

Пример ответа:
```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huX2RvZSIsImV4cCI6MTczNTIxMzU3Mn0.JyxVg7NjihW2UXVtYwTHngxDQ_POnmmJezQM8Mu9tRc",
    "token_type": "bearer"
}
```


### 7.2 Пример использования

Для запуска ML-модели классификации вина выполните запрос по маршруту `/make_inference` с параметрами features
В данном случае мы передаем 13 признаком float формата.
Для доступа к маршруту, поместите ранее полученный токен в заголовок `Authorization`.

Пример curl-запроса:
```
curl --location 'http://localhost:8000/make_inference' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huX2RvZSIsImV4cCI6MTczNTIxMzU3Mn0.JyxVg7NjihW2UXVtYwTHngxDQ_POnmmJezQM8Mu9tRc' \
--header 'Content-Type: application/json' \
--data '{
    "features": [13.72, 1.36, 2.29, 19.5, 96.5, 1.9, 3.26, 0.33, 1.8, 5.04, 0.86, 4.5, 890]
}'
```

Пример ответа:
```
{
    "prediction": 1,
    "user": {
        "username": "otus"
    }
}
```
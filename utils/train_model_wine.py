from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import joblib
import logging
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

CONFIG = {"MODELDIR": "models/"}

model_dir = CONFIG.get("MODELDIR")
os.makedirs(model_dir, exist_ok=True)


def train_model():
    try:
        logger.info("Создание модели...")
        data = load_wine()
        X, y = data.data, data.target

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        logger.info("Обучение модели...")
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)

        logger.info("Модель обучена. Оценка качества модели...")
        y_pred = model.predict(X_test)
        logger.info(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")

        model_path = os.path.join(model_dir, "wine_model.pkl")
        logger.info(f"Сохранение модели в файл {model_path}...")
        joblib.dump(model, model_path)
        logger.info("Модель успешно сохранена.")

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    train_model()

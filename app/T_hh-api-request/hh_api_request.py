import requests  # Основная библиотека для HTTP-запросов
import json      # Для работы с JSON-форматом
from time import sleep  # Для паузы между запросами

def get_vacancies_from_hh(search_text="Python", experience="noExperience", work_format="REMOTE", area=113, per_page=10):
    """
    Функция для получения вакансий с HeadHunter API.
    
    Параметры:
    search_text (str): Ключевые слова для поиска (например, "Python", "Data Science")
    experience (str): Уровень опыта. Ключевые варианты:
        - "noExperience" — Нет опыта (Junior)
        - "between1And3" — От 1 до 3 лет (Middle)
        - "between3And6" — От 3 до 6 лет (Senior)
        - "moreThan6" — Более 6 лет
    area (int): Регион. 113 — Россия, 1 — Москва, 2 — СПб.
    per_page (int): Количество вакансий на странице (макс. 100).
    """
    
    # 1. Базовый URL эндпоинта API HH для вакансий
    BASE_URL = "https://api.hh.ru/vacancies"
    
    # 2. Формируем параметры запроса (то, что обычно видно в URL после "?")
    # Эти параметры API HH принимает в GET-запросе.
    params = {
        "text": f"NAME:({search_text})",  # Ищем в названии вакансии
        "experience": experience,
        "area": area,
        "per_page": per_page,  # Сколько вакансий на странице
        "page": 0,  # Номер страницы (начинается с 0)
        "only_with_salary": False,  # Можно поставить True, если нужны только с зарплатой
        "period": 30,  # Количество дней для поиска (1, 7, 30)
        "work_format": work_format,
    }
    
    # 3. Отправляем GET-запрос с нашими параметрами
    # Важно добавить User-Agent, чтобы сервер не принял за бота
    headers = {
        "User-Agent": "HHAnalyst/0.1 (sweeetdozer@gmail.com)"  # Указать email
    }
    
    print(f"Запрашиваю вакансии по запросу: '{search_text}' для опыта: '{experience}'...")
    
    try:
        response = requests.get(BASE_URL, params=params, headers=headers)
        
        # 4. Проверяем статус ответа. 200 — успешно.
        response.raise_for_status()  # Выбросит исключение при ошибке HTTP (4xx, 5xx)
        
        # 5. Преобразуем ответ из JSON в Python-словарь
        data = response.json()
        
        # 6. Основные поля ответа:
        print(f"\n=== Статус ===")
        print(f"Найдено вакансий: {data.get('found', 0)}")
        print(f"Страниц: {data.get('pages', 0)}")
        print(f"Текущая страница: {data.get('page', 0) + 1}")
        
        # 7. Пробегаемся по полученным вакансиям (первые 3 для примера)
        print(f"\n=== Примеры вакансий (первые 3) ===")
        for i, item in enumerate(data.get("items", [])[:3]):
            vacancy = item
            salary_info = vacancy.get("salary")
            salary_str = "Не указана"
            requirement = vacancy.get("snippet").get("requirement", "Не указано")
            responsibility = vacancy.get("snippet").get("responsibility", "Не указано")
            
            # Обрабатываем информацию о зарплате (может быть сложной структурой)
            if salary_info:
                from_salary = salary_info.get("from")
                to_salary = salary_info.get("to")
                currency = salary_info.get("currency", "")
                mode = vacancy.get("salary_range", {}).get("mode", {}).get("name", "Не указано")
                frequency = vacancy.get("salary_range", {}).get("frequency").get("name", "Не указано")
                salary_str = f"{from_salary if from_salary else '?'} - {to_salary if to_salary else '?'} {currency}  {mode}/{frequency}"
            
            print(f"{i+1}. {vacancy.get('name')}")
            print(f"   Зарплата: {salary_str}")
            print(f"   Работодатель: {vacancy.get('employer', {}).get('name')}")
            print(f"   Ссылка: {vacancy.get('alternate_url')}")
            print(f"   Требования: {requirement}")
            print(f"   Обязаности: {responsibility}")
        
        # 8. Сохраняем полный ответ в JSON-файл для дальнейшего анализа
        filename = f"hh_vacancies_{search_text}_{experience}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Полные данные сохранены в файл: {filename}")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None

# Если файл запускается напрямую, а не импортируется
if __name__ == "__main__":
    # Пример 1: Ищем Python-вакансии для джунов по России
    data = get_vacancies_from_hh(
        search_text="Python", 
        experience="noExperience", 
        area=113,  # Россия
        per_page=20  # Возьмем поменьше для теста
    )
    
    # Пауза 1 секунда, чтобы не нагружать сервис
    sleep(1)
    
    # Пример 2: Можно искать другие технологии
    # get_vacancies_from_hh("Data Science", "between1And3", 1, 10)
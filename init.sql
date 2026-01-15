-- Убедимся, что база существует
CREATE DATABASE IF NOT EXISTS hh_vacancies CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Даем права пользователю
GRANT ALL PRIVILEGES ON hh_vacancies.* TO 'hh_user'@'%';

FLUSH PRIVILEGES;
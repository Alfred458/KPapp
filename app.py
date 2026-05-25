import streamlit as st
from datetime import datetime
import pandas as pd

# Конфигурация страницы
st.set_page_config(
    page_title="Образовательная платформа",
    page_icon="📚",
    layout="wide"
)

# Данные пользователей (в реальном приложении хранить в БД)
USERS = {
    "student": {
        "password": "1",
        "role": "student",
        "name": "Иван Петров"
    },
    "teacher": {
        "password": "1",
        "role": "teacher",
        "name": "Анна Смирнова"
    },
    "admin": {
        "password": "1",
        "role": "admin",
        "name": "Администратор"
    }
}


# Функция инициализации состояния сессии
def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    if "page" not in st.session_state:
        st.session_state.page = "main"


# Функция аутентификации
def authenticate(username, password):
    if username in USERS and USERS[username]["password"] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.user_role = USERS[username]["role"]
        st.session_state.user_name = USERS[username]["name"]
        return True
    return False


# Функция выхода
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.user_name = None
    st.session_state.page = "main"
    st.rerun()


def student_dashboard():
    # Меню студента - отдельные кнопки в сайдбаре
    with st.sidebar:
        st.markdown("### 📚 Навигация")
        if st.button("📚 Мои курсы", use_container_width=True):
            st.session_state.page = "my_courses"
        if st.button("📝 Задания", use_container_width=True):
            st.session_state.page = "tasks"
        if st.button("📊 Прогресс", use_container_width=True):
            st.session_state.page = "progress"
        # НОВЫЕ ФИЧИ ДЛЯ СТУДЕНТА
        if st.button("💬 Чат с преподавателем", use_container_width=True):
            st.session_state.page = "chat"
        if st.button("🏆 Достижения", use_container_width=True):
            st.session_state.page = "achievements"

    # Отображение выбранной страницы
    if st.session_state.page == "my_courses":
        st.title("Мои курсы")
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.subheader("Python для начинающих")
                st.progress(0.65)
                st.write("Прогресс: 65%")
                if st.button("Продолжить обучение", key="course1"):
                    st.info("Запуск курса...")

            with st.container(border=True):
                st.subheader("Lua для начинающих")
                st.progress(0.13)
                st.write("Прогресс: 13%")
                if st.button("Продолжить обучение", key="course2"):
                    st.info("Запуск курса...")

        with col2:
            with st.container(border=True):
                st.subheader("Web разработка")
                st.progress(0.30)
                st.write("Прогресс: 30%")
                if st.button("Продолжить обучение", key="course3"):
                    st.info("Запуск курса...")

            with st.container(border=True):
                st.subheader("C#")
                st.progress(0.50)
                st.write("Прогресс: 50%")
                if st.button("Продолжить обучение", key="course4"):
                    st.info("Запуск курса...")

    elif st.session_state.page == "tasks":
        st.header("Активные задания")

        with st.container(border=True):
            st.subheader("Домашнее задание #1")
            st.write("Создать простое веб-приложение на Streamlit")
            st.caption("Срок сдачи: 15.04.2026")
            uploaded_file = st.file_uploader("Выберите файл", type=['py', 'ipynb'], key="task1")
            if uploaded_file:
                st.success("Файл загружен!")

        with st.container(border=True):
            st.subheader("Тестирование")
            st.write("Пройти тест по теме 'Функции'")
            st.caption("Срок сдачи: 10.04.2026")
            if st.button("Начать тест"):
                st.info("Тест начат!")

        with st.container(border=True):
            st.subheader("Домашнее задание 'Основы Python'")
            st.write("Создать простой проект")
            st.caption("Срок сдачи: 15.04.2026")
            uploaded_file2 = st.file_uploader("Выберите файл", type=['py', 'ipynb'], key="task2")
            if uploaded_file2:
                st.success("Файл загружен!")

    elif st.session_state.page == "progress":
        st.header("Мой прогресс")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Пройдено курсов", "2", delta="+1")
            st.metric("Средняя оценка", "4.7", delta="+0.2")
        with col2:
            st.metric("Выполнено заданий", "8/12", delta="2")
            st.metric("Общее время обучения", "24 часа", delta="+3ч")

        st.subheader("График успеваемости")
        progress_data = pd.DataFrame({
            'Дата': ['Янв', 'Фев', 'Мар', 'Апр', 'Май'],
            'Прогресс': [65, 30, 45, 70, 85]
        })
        st.line_chart(progress_data.set_index('Дата'))

    # НОВАЯ ФИЧА 1: Чат с преподавателем
    elif st.session_state.page == "chat":
        st.header("💬 Чат с преподавателем")

        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {"role": "teacher", "message": "Здравствуйте! Задавайте ваши вопросы по курсу", "time": "10:00"}
            ]

        # Отображение сообщений
        for msg in st.session_state.chat_messages:
            if msg["role"] == "student":
                st.chat_message("user").write(f"**Вы** ({msg['time']}): {msg['message']}")
            else:
                st.chat_message("assistant").write(f"**Преподаватель** ({msg['time']}): {msg['message']}")

        # Ввод нового сообщения
        new_message = st.chat_input("Введите ваше сообщение...")
        if new_message:
            current_time = datetime.now().strftime("%H:%M")
            st.session_state.chat_messages.append({
                "role": "student",
                "message": new_message,
                "time": current_time
            })
            # Автоответ преподавателя
            st.session_state.chat_messages.append({
                "role": "teacher",
                "message": "Спасибо за вопрос! Я отвечу в ближайшее время.",
                "time": current_time
            })
            st.rerun()

    # НОВАЯ ФИЧА 2: Достижения
    elif st.session_state.page == "achievements":
        st.header("🏆 Мои достижения")

        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.markdown("🎯")
                st.subheader("Первые шаги")
                st.write("Пройден первый курс")
                st.progress(1.0)
                st.success("Получено!")

        with col2:
            with st.container(border=True):
                st.markdown("⚡")
                st.subheader("Отличник")
                st.write("Средний балл выше 4.5")
                st.progress(0.8)
                st.info("Осталось немного!")

        with col3:
            with st.container(border=True):
                st.markdown("📚")
                st.subheader("Книголюб")
                st.write("Изучено 5 курсов")
                st.progress(0.4)
                st.warning("В процессе...")


def teacher_dashboard():
    st.title(f"👨‍🏫 Добро пожаловать, {st.session_state.user_name}!")
    st.markdown("---")

    # Меню преподавателя - отдельные кнопки в сайдбаре
    with st.sidebar:
        st.markdown("### 👨‍🏫 Панель преподавателя")
        if st.button("📤 Загрузить курс", use_container_width=True):
            st.session_state.page = "upload_course"
        if st.button("📋 Список студентов", use_container_width=True):
            st.session_state.page = "student_list"
        if st.button("📊 Оценки", use_container_width=True):
            st.session_state.page = "grades"
        # НОВЫЕ ФИЧИ ДЛЯ ПРЕПОДАВАТЕЛЯ
        if st.button("📅 Расписание занятий", use_container_width=True):
            st.session_state.page = "schedule"
        if st.button("📈 Аналитика успеваемости", use_container_width=True):
            st.session_state.page = "analytics"

    # Отображение выбранной страницы
    if st.session_state.page == "upload_course":
        st.header("Загрузка нового курса")

        with st.form("upload_course"):
            course_name = st.text_input("Название курса")
            course_description = st.text_area("Описание курса")
            course_materials = st.file_uploader("Материалы курса", accept_multiple_files=True)
            submit = st.form_submit_button("Загрузить курс")

            if submit and course_name:
                st.success(f"Курс '{course_name}' успешно загружен!")
                if course_materials:
                    st.info(f"Загружено материалов: {len(course_materials)}")

    elif st.session_state.page == "student_list":
        st.header("Список студентов")

        students = [
            {"name": "Иван Петров", "group": "ПИ-101", "email": "ivan@example.com", "avg_grade": 4.5},
            {"name": "Мария Сидорова", "group": "ПИ-101", "email": "maria@example.com", "avg_grade": 4.8},
            {"name": "Алексей Иванов", "group": "ПИ-102", "email": "alex@example.com", "avg_grade": 4.2},
        ]

        for student in students:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                with col1:
                    st.write(f"**{student['name']}**")
                with col2:
                    st.write(f"Группа: {student['group']}")
                with col3:
                    st.write(f"📧 {student['email']}")
                with col4:
                    st.write(f"⭐ {student['avg_grade']}")

    elif st.session_state.page == "grades":
        st.header("Управление оценками")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Выбор студента")
            student = st.selectbox("Студент", ["Иван Петров", "Мария Сидорова", "Алексей Иванов"])

        with col2:
            st.subheader("Выбор курса")
            course = st.selectbox("Курс", ["Python", "Web разработка", "Базы данных"])

        st.subheader("Оценки")
        grade = st.slider("Оценка", 0, 5, 4)
        comment = st.text_area("Комментарий")

        if st.button("Сохранить оценку"):
            st.success(f"Оценка {grade} для {student} по курсу {course} сохранена!")

    # НОВАЯ ФИЧА 1: Расписание занятий
    elif st.session_state.page == "schedule":
        st.header("📅 Расписание занятий")

        schedule_data = pd.DataFrame({
            'Время': ['10:00', '12:00', '14:00', '16:00'],
            'Понедельник': ['Python', 'Web', 'Перерыв', 'Базы данных'],
            'Вторник': ['Алгоритмы', 'Python', 'Перерыв', 'Консультация'],
            'Среда': ['Web', 'Базы данных', 'Перерыв', 'Практика'],
            'Четверг': ['Python', 'Алгоритмы', 'Перерыв', 'Web'],
            'Пятница': ['Тестирование', 'Консультация', 'Перерыв', 'Python']
        })

        st.dataframe(schedule_data, use_container_width=True)

        st.subheader("Добавить занятие")
        with st.form("add_lesson"):
            col1, col2 = st.columns(2)
            with col1:
                day = st.selectbox("День недели", ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"])
                time = st.time_input("Время")
            with col2:
                subject = st.text_input("Предмет")
                room = st.text_input("Аудитория")

            if st.form_submit_button("Добавить занятие"):
                st.success(f"Занятие по {subject} добавлено на {day} в {time}")

    # НОВАЯ ФИЧА 2: Аналитика успеваемости
    elif st.session_state.page == "analytics":
        st.header("📈 Аналитика успеваемости")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Средний балл группы", "4.5", delta="+0.3")
        with col2:
            st.metric("Успеваемость", "92%", delta="+5%")
        with col3:
            st.metric("Посещаемость", "88%", delta="-2%")

        st.subheader("Успеваемость по курсам")
        courses_data = pd.DataFrame({
            'Курс': ['Python', 'Web разработка', 'Базы данных', 'Алгоритмы'],
            'Средний балл': [4.7, 4.3, 4.5, 4.2]
        })
        st.bar_chart(courses_data.set_index('Курс'))

        st.subheader("Успеваемость студентов")
        student_performance = pd.DataFrame({
            'Студент': ['Иван П.', 'Мария С.', 'Алексей И.', 'Ольга К.', 'Дмитрий Р.'],
            'Python': [5, 5, 4, 4, 3],
            'Web': [4, 5, 4, 5, 4],
            'Базы данных': [5, 4, 4, 5, 4],
            'Средний': [4.67, 4.67, 4.0, 4.67, 3.67]
        })
        st.dataframe(student_performance, use_container_width=True)


def admin_dashboard():
    st.title(f"⚙️ Панель администратора")
    st.markdown(f"**Добро пожаловать, {st.session_state.user_name}!**")
    st.markdown("---")

    # Меню администратора - отдельные кнопки в сайдбаре
    with st.sidebar:
        st.markdown("### ⚙️ Управление системой")
        if st.button("👥 Управление пользователями", use_container_width=True):
            st.session_state.page = "user_management"
        if st.button("📊 Статистика", use_container_width=True):
            st.session_state.page = "statistics"
        if st.button("⚙️ Настройки системы", use_container_width=True):
            st.session_state.page = "settings"
        # НОВЫЕ ФИЧИ ДЛЯ АДМИНИСТРАТОРА
        if st.button("📋 Логи системы", use_container_width=True):
            st.session_state.page = "logs"
        if st.button("💾 Резервное копирование", use_container_width=True):
            st.session_state.page = "backup"

    # Отображение выбранной страницы
    if st.session_state.page == "user_management":
        st.header("Управление пользователями")

        # Список пользователей
        st.subheader("Список пользователей")

        users_data = [
            {"username": "student", "name": "Иван Петров", "role": "student", "status": "active",
             "last_login": "2024-01-15"},
            {"username": "teacher", "name": "Анна Смирнова", "role": "teacher", "status": "active",
             "last_login": "2024-01-16"},
            {"username": "admin", "name": "Администратор", "role": "admin", "status": "active",
             "last_login": "2024-01-16"},
        ]

        for user in users_data:
            with st.container(border=True):
                col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 1.5, 1, 1.5, 1])
                with col1:
                    st.write(user["username"])
                with col2:
                    st.write(user["name"])
                with col3:
                    st.write(user["role"])
                with col4:
                    st.write(user["status"])
                with col5:
                    st.write(user["last_login"])
                with col6:
                    if st.button("✏️", key=f"edit_{user['username']}"):
                        st.info(f"Редактирование {user['username']}")

        # Добавление нового пользователя
        with st.expander("➕ Добавить пользователя"):
            with st.form("add_user"):
                new_username = st.text_input("Логин")
                new_password = st.text_input("Пароль", type="password")
                new_name = st.text_input("Полное имя")
                new_role = st.selectbox("Роль", ["student", "teacher", "admin"])
                submit = st.form_submit_button("Добавить")

                if submit and new_username:
                    st.success(f"Пользователь {new_username} добавлен!")

    elif st.session_state.page == "statistics":
        st.header("Статистика системы")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Всего пользователей", "24", delta="+3")
        with col2:
            st.metric("Активных курсов", "12", delta="+2")
        with col3:
            st.metric("Всего заданий", "45", delta="+5")
        with col4:
            st.metric("Активность сегодня", "156", delta="+12")

        st.subheader("Активность пользователей по дням")
        activity_data = pd.DataFrame({
            'День': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
            'Активность': [120, 135, 150, 145, 160, 95, 80]
        })
        st.line_chart(activity_data.set_index('День'))

        st.subheader("Распределение пользователей по ролям")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Студенты", "180")
        with col2:
            st.metric("Преподаватели", "15")
        st.caption(f"Администраторы: 5")

    elif st.session_state.page == "settings":
        st.header("Настройки системы")

        with st.form("system_settings"):
            st.subheader("Общие настройки")
            site_name = st.text_input("Название платформы", "Образовательная платформа")
            theme = st.selectbox("Тема", ["Светлая", "Темная", "Системная"])
            email_notifications = st.checkbox("Включить email уведомления", value=True)

            st.subheader("Безопасность")
            session_timeout = st.number_input("Таймаут сессии (минуты)", min_value=5, max_value=120, value=30)
            two_factor_auth = st.checkbox("Двухфакторная аутентификация", value=False)

            if st.form_submit_button("Сохранить настройки"):
                st.success("Настройки сохранены!")

    # НОВАЯ ФИЧА 1: Логи системы
    elif st.session_state.page == "logs":
        st.header("📋 Логи системы")

        tab1, tab2, tab3 = st.tabs(["Действия пользователей", "Ошибки", "Входы в систему"])

        with tab1:
            logs_data = pd.DataFrame({
                'Время': ['2024-01-16 10:30', '2024-01-16 11:45', '2024-01-16 14:20'],
                'Пользователь': ['student', 'teacher', 'admin'],
                'Действие': ['Загрузил задание', 'Добавил курс', 'Изменил настройки'],
                'IP адрес': ['192.168.1.1', '192.168.1.2', '192.168.1.3']
            })
            st.dataframe(logs_data, use_container_width=True)

        with tab2:
            st.info("Системных ошибок не обнаружено за последние 24 часа")

        with tab3:
            login_logs = pd.DataFrame({
                'Время': ['2024-01-16 09:00', '2024-01-16 10:15', '2024-01-16 11:30'],
                'Пользователь': ['ivan', 'maria', 'alex'],
                'Статус': ['Успешно', 'Успешно', 'Неудачно'],
                'IP адрес': ['192.168.1.10', '192.168.1.11', '192.168.1.12']
            })
            st.dataframe(login_logs, use_container_width=True)

        if st.button("Очистить логи"):
            st.warning("Логи очищены!")

    # НОВАЯ ФИЧА 2: Резервное копирование
    elif st.session_state.page == "backup":
        st.header("💾 Резервное копирование")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Создать резервную копию")
            backup_type = st.selectbox("Тип резервной копии",
                                       ["Полная", "Инкрементальная", "Только данные пользователей"])
            backup_comment = st.text_area("Комментарий к резервной копии")

            if st.button("Создать резервную копию", type="primary"):
                with st.spinner("Создание резервной копии..."):
                    import time
                    time.sleep(2)
                st.success(f"Резервная копия ({backup_type}) успешно создана!")
                st.info("Размер: 245 MB")

        with col2:
            st.subheader("Восстановление")
            backup_file = st.file_uploader("Выберите файл резервной копии", type=['zip', 'sql', 'bak'])
            if backup_file:
                if st.button("Восстановить из копии", type="secondary"):
                    st.warning("⚠️ Восстановление заменит текущие данные!")
                    confirm = st.checkbox("Я подтверждаю восстановление данных")
                    if confirm:
                        st.success("Данные восстановлены успешно!")

        st.subheader("📋 Список резервных копий")
        backups = pd.DataFrame({
            'Дата': ['2024-01-15 10:00', '2024-01-14 10:00', '2024-01-13 10:00'],
            'Тип': ['Полная', 'Инкрементальная', 'Полная'],
            'Размер': ['250 MB', '45 MB', '248 MB'],
            'Комментарий': ['Еженедельное', 'Ежедневное', 'Перед обновлением']
        })
        st.dataframe(backups, use_container_width=True)


# Главная функция
def main():
    init_session_state()

    # Если не авторизован, показываем форму входа
    if not st.session_state.authenticated:
        st.title("🔐 Вход в образовательную платформу")
        st.markdown("---")

        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            with st.container(border=True):
                st.subheader("Авторизация")
                username = st.text_input("Логин")
                password = st.text_input("Пароль", type="password")

                if st.button("Войти", use_container_width=True):
                    if authenticate(username, password):
                        st.success("Вход выполнен успешно!")
                        st.rerun()
                    else:
                        st.error("Неверный логин или пароль")

                st.markdown("---")
                st.caption("Тестовые учетные записи:")
                st.caption("📘 student / 1")
                st.caption("👨‍🏫 teacher / 1")
                st.caption("⚙️ admin / 1")

    # Если авторизован, показываем интерфейс
    else:
        # Сайдбар с информацией о пользователе
        with st.sidebar:
            st.write(f"**Пользователь:** {st.session_state.user_name}")
            st.write(f"**Роль:** {st.session_state.user_role}")

            if st.button("🚪 Выйти", use_container_width=True):
                logout()

            st.markdown("---")

        # Отображаем соответствующий дашборд
        if st.session_state.user_role == "student":
            student_dashboard()
        elif st.session_state.user_role == "teacher":
            teacher_dashboard()
        elif st.session_state.user_role == "admin":
            admin_dashboard()


if __name__ == "__main__":
    main()
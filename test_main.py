import pytest
from main import LogReport


@pytest.fixture
def fix_path():
    path1 = "logs/app1.log"
    path2 = "logs/app2.log"
    return [path1, path2]


@pytest.fixture
def fix_log():
    log_text1 = "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ " \
    "204 OK [192.168.1.59]2025-03-28 12:21:51,000 INFO django.request: GET " \
    "/admin/dashboard/ 200 OK [192.168.1.68]2025-03-28 12:40:47,000 CRITICAL " \
    "django.core.management: DatabaseError: Deadlock detected2025-03-28 12:25:45,000 " \
    "DEBUG django.db.backends: (0.41) SELECT * FROM 'products' WHERE id = 4;2025-03-28 " \
    "12:03:09,000 DEBUG django.db.backends: (0.19) SELECT * FROM 'users' WHERE id = 32;"

    log_text2 = "2025-03-27 12:29:35,000 INFO django.request: GET /api/v1/orders/ 204 OK " \
    "[192.168.1.67]2025-03-27 12:06:15,000 WARNING django.security: IntegrityError:" \
    " duplicate key value violates unique constraint2025-03-27 12:10:49,000 CRITICAL " \
    "django.core.management: OSError: No space left on device2025-03-27 12:42:07,000 INFO " \
    "django.request: GET /api/v1/users/ 201 OK [192.168.1.22]2025-03-27 12:44:47,000 INFO " \
"django.request: GET /api/v1/payments/ 204 OK [192.168.1.57]"
    return [log_text1, log_text2]


@pytest.fixture
def fix_rows():
    return ["django.request: GET /api/v1/payments/ 204 OK [192.168.1.57]"]

@pytest.fixture
def fix_matrix():
    cleaned_handlers = ["/api/v1/reviews/", "/admin/dashboard/", "/api/v1/users/", "/api/v1/payments/"]
    levels =["DEBUG", "INFO", "WARNING", "ERROR","CRITICAL"]
    total= 0
    rows = ["2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/"
    "204 OK ", "[192.168.1.59]2025-03-28 12:21:51,000 INFO django.request: GET " \
    "/admin/dashboard/ 200 OK ", "[192.168.1.68]2025-03-28 12:40:47,000 CRITICAL " \
    "django.core.management: DatabaseError: Deadlock detected2025-03-28", " 12:25:45,000 " \
    "DEBUG django.db.backends: (0.41) SELECT * FROM 'products' WHERE id = 4;2025-03-28"," " \
    "12:03:09,000 DEBUG django.db.backends: (0.19) SELECT * FROM 'users' WHERE id = 32;", "2025-03-27 12:29:35,000 INFO django.request: GET /api/v1/orders/ 204 OK " \
    "[192.168.1.67]2025-03-27 12:06:15,000 WARNING django.security: IntegrityError:" \
    " duplicate key value violates unique constraint2025-03-27"," 12:10:49,000 CRITICAL " \
    "django.core.management: OSError: No space left on device2025-03-27"," 12:42:07,000 INFO " \
    "django.request: GET /api/v1/users/ 201 OK"," [192.168.1.22]2025-03-27 12:44:47,000 INFO " \
"django.request: GET /api/v1/payments/ 204 OK [192.168.1.57]"
]

    return [cleaned_handlers, levels, rows, total]

#   Тестирование получения хэндлеров из строк
def test_get_unique_handlers(fix_rows):
    lr = LogReport()
    rows = ["django.request: GET /api/v1/payments/ 204 OK [192.168.1.57]"]
    res = lr.get_unique_handler(rows)
    assert res == ["/api/v1/payments/"]

#   Тестирование создания таблицы
def test_create_matrix(fix_matrix):
    matrix = [[0]*5 for _ in range(len(fix_matrix[0]))]
    excepted_matrix = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    assert matrix == excepted_matrix

#   Тестирование правильного заполнения матрицы
def test_fill_matrix(fix_matrix):
    lr = LogReport()
    matrix = [[0]*5 for _ in range(len(fix_matrix[0]))]
    res = lr.fill_matrix(matrix, fix_matrix[0], fix_matrix[1], fix_matrix[2], fix_matrix[3])
    res = res[0]
    expected_matrix = [[0,1,0,0,0],[0,1,0,0,0],[0,1,0,0,0],[0,1,0,0,0]]
    assert res == expected_matrix


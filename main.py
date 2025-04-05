import os, re, sys

levels =["DEBUG", "INFO", "WARNING", "ERROR","CRITICAL"]
pattern = r"/[^/\s]+(?:/[^/\s]+)*/"     #   Паттерн для поиска в строках хендлеров
handlers=list()
total=0     #   Счет количества запросов к хендлерам

class LogReport:

    #   Функция разбивает логи на строки
    def split_values(self, paths_to_logs: list) -> list:
         all_rows = list()
         for log in paths_to_logs:
             try:
                 if log != "--report":
                    with open(log, "r") as text:
                        rows=text.read()
                        all_rows.extend(rows.split("\n"))
             except FileNotFoundError:
                continue


         return all_rows

    #   Создает список уникальных ручек
    def get_unique_handler(self, all_rows: list) -> list:
        for value in all_rows:
                matches = re.findall(pattern, value)
                if matches != []:
                    if matches[0] not in handlers:
                        handlers.append(matches[0])
        return handlers

    #   Функция заполняет матрицу значениями по каждому уровню логирования
    def fill_matrix(self, matrix: list, handlers: list, levels: list, rows: list, total: int) -> tuple:
        for value in rows:
            handler_index = None
            level_index = None
            for handler in handlers:
                if handler in value:
                    handler_index=handlers.index(handler)
                    break
                else:
                    handler_index = None
               
            for level in levels:
                if level in value:
                    level_index = levels.index(level)
            if handler_index != None:
              matrix[handler_index][level_index] += 1
              total+=1

        return matrix, total

    #    Функция выполняет все методы класса
    def get_filled_matrix(self) -> tuple:
        paths_to_logs = sys.argv[1:]

        log_rep = LogReport()

        raw_handlers=log_rep.split_values(paths_to_logs)

        cleaned_handlers=sorted(log_rep.get_unique_handler(raw_handlers))

        handlers_copy = sorted(cleaned_handlers.copy())

        matrix = [[0]*5 for _ in range(len(cleaned_handlers))]

        filler_matrix = log_rep.fill_matrix(matrix, cleaned_handlers, raw_handlers, total)

        total_for_level = []

        for i in range(len(levels)):
            temp_num = 0
            for j in range(len(filler_matrix[0])):

                temp_num += filler_matrix[0][j][i]
            total_for_level.append(temp_num)



        return filler_matrix, handlers_copy, total_for_level


def main():

    # Функция парсит аргументы переданные во время запуска программы
    files_paths = sys.argv[1:]
    for path in files_paths[:]:
        if "--report" in path:
            name_of_report = path.split("--report ")
            files_paths.remove(path)
            break
        elif os.path.exists(path):
            continue
        else:
            print(f"Нет файла {path}")

    get_filled_matrix = LogReport().get_filled_matrix

    print("Total requests: ", get_filled_matrix()[0][1])

    data = tuple(get_filled_matrix()[0])
    list_handlers=list(handlers)

    #   Настройка ширины столбцов вывода
    column_widths = [20, 20, 20, 20, 20, 13]
    
    # Функция вывода строки
    def print_row(row):
        print("  ".join(f"{str(row[i]):<{column_widths[i]}}" for i in range(len(row))))
          
    # Печать таблицы
    print("HANDLER" + " " * column_widths[5] + "  "+"  ".join(f"{str(levels[i]):<{column_widths[i]}}" for i in range(len(levels))))
    for i in range(len(list_handlers)):
        print_row([get_filled_matrix()[1][i]] + data[0][list_handlers.index(list_handlers[i])])
    level_values = get_filled_matrix()[0][0]
    print("\n"+" " * column_widths[0] + "  "+"  ".join(f"{str(get_filled_matrix()[2][i]):<{column_widths[i]}}" for i in range(len(levels))))

    
if __name__=="__main__":
    main()

# Виджет банковских операций по карте/счету

## Данный виджет предназначен для банковских операций клиента: 
1. Маскировка номера карты клиента;
2. Маскировка номера счета клиента; 
3. Умеет принимать на вход строку с датой в одном и 
возвращает строку с датой в формате "ДД.ММ.ГГГГ"

# Установка

Клонируйте репозиторий:

``` git clone https://github.com/vasilenko8021978-tech/bank_operation ```

**Установите зависимости, используя менеджер пакетов `poetry`:**
    
``` poetry install```

## Использование

Виджет предоставляет следующие основные функции:

 1. `get_mask_card_number(card_number)`   
Функция возвращает скрытый номер карты в формате:  
`1234 56** **** 7890`  
 2. `get_mask_account(account_number)`  
Функция возвращает скрытый номер счета в формате:  
`**1234`  
 3. `mask_account_card(name_card)`  
Функция определяет формат данных счет/карта, далее с помощью соответствующих   
функций `1` и `2` скрывает номер. Возвращает в формате:  
`ИМЯ КАРТЫ 1234 56** **** 7890`  
или  
`счет ** 7890`  
 4. `get_date(time_card)`  
Функция возвращает строку с датой в формате:  
`ДД.ММ.ГГГГ`  
 5. `filter_by_state(list_state, key_state = "EXECUTED")`  
Функция фильтрует словари по заданному значению для ключа `state`  
 6. `sort_by_date(list_dict, reduce)`  
Функция возвращает по умолчанию отсортированный по убыванию список по дате
7. filter_by_currency(transactions)
Функция возвращает итератор, который поочередно выдает транзакции
8. transaction_description(transactions)
Генератор, который возвращает описание каждой транзакции по очереди
9. card_number_generator(start, end)
Генератор, который выдает номера банковских карт в формате 'XXXX XXXX XXXX XXXX'
10. log (filename)
Декоратор для автоматического логирования выполнения функции.
11. Добавлена функция clean_transaction_data и read_transactions_from_json которые принимают на вход путь до JSON-файла
и возвращают список словарей с данными о финансовых транзакциях
12. добавлена функция get_exchange_rate, которая получает текущий курс обмена валют с использованием Exchange Rates Data API
13. добавлена функция convert_amount_to_rubles, которая конвертирует в рубли 
14. добавлена функция get_transaction_amount_in_rubles  которая извлекает сумму транзакции и конвертирует в рубли

### Тесты

## Фикстуры для filter_by_state

1. transactions_mixed
Фикстура задает список транзакций с разными статусами

2. empty_list 
Фикстура задает пустой список

3. transactions_no_target_state
Фикстура задает список без транзакций с определенным статусом

4. transactions_single
Фикстура задает список с одной транзакцией.

## Фикстуры для sort_by_date

1. transactions_unsorted
Фикстура задает список транзакций с неотсортированными датами

2. transactions_same_dates
Фикстура задает список транзакций с одинаковыми датами.

3. transactions_invalid_dates
Фикстура задает список транзакций с некорректными форматами дат

4. transactions_missing_date
Фикстура задает список транзакций без ключа 'date'

## Блок параметризованных тестов test_masks.py

1. функция test_get_mask_card_number проверяет различные ситуации с картами
2. функция test_get_mask_account проверяет различные ситуации со счетами

## Блок параметризованных тестов test_widget.py

1. функция test_mask_account_card проверяет различные граничные значения функции mask_account_card
2. функции test_get_date, test_get_date_short_string, test_get_date_wrong_separator_at_position_4, 
test_get_date_wrong_separator_at_position_7,test_get_date_index_error_in_try_block тестируют разные значения get_date

## Блок параметризованных тестов test_processing.py

1. Функция test_filter_by_state_valid производит тест фильтрации по существующим статусам
2. Функция test_filter_by_state_default производит тест фильтрации со значением по умолчанию (EXECUTED)  
3. Функция test_filter_by_state_not_found производит тест фильтрации при отсутствии словарей с указанным статусом
4. Функция test_filter_by_state_empty_list производит тест фильтрации пустого списка
5. Функция test_filter_by_state_single_item производит тест фильтрации списка с одной транзакцией
6. Функция test_sort_by_date_empty_list производит тест сортировки пустого списка
7. Функция test_sort_by_date_missing_date_key производит тест обработки ключа "date"
8. Функция test_sort_by_date_invalid_date_format производит тест функции с некорректными датами
9. Функция test_sort_by_date_parametrized проверяет правильность сортировки

## Блок параметризованных тестов test_decorators

1. test_log_decorator_with_timestap_console тест логирования с временной меткой в консоль
2. test_log_decorator_with_timestamp_file тест логирования с временной меткой в файл
3. test_mask_account_card_with_log_decorator_success тест успешного выполнения функции mask_account_card с декоратором @log
4. test_mask_account_card_with_log_decorator_card_number тест маскирования номера карты с декоратором
5. test_mask_account_card_with_log_decorator_account тест маскирования номера счёта с декоратором
6. test_mask_account_card_with_log_decorator_empty_string тест обработки пустой строки с декоратором
7. test_mask_account_card_with_log_decorator_invalid_format тест обработки неверного формата с декоратором
8. test_mask_account_card_with_log_decorator_non_digit тест обработки нецифровых символов с декоратором
9. test_mask_account_card_with_log_to_file  тест логирования в файл
10. test_mask_account_card_with_log_decorator_and_error тест обработки ошибок функции mask_account_card с декоратором

Покрытие тестами 96 процентов

## Фикстура для filter_by_currency, transaction_description
sample_transaction
Фикстура задает транзакции с обычными статусами

## Тесты для filter_by_currency

1. test_filter_by_currency_usd производит тестирование фильтрации транзакций в USD
2. test_filter_by_currency_eur производит тестирование фильтрации транзакций в EUR
3. test_filter_by_currency_rub производит тестирование фильтрации транзакций в RUB
4. test_filter_by_currency_no_matches производит тестирование фильтрации, 
когда транзакции в заданной валюте отсутствуют
5. test_filter_by_currency_empty_list производит тестирование работы с пустым списком
6. test_filter_by_currency_non_currency_code производит тестирование с пустым или None кодом валюты

## Тесты для transaction_description

1. test_transaction_description проверяет, что функция возвращает корректные описания для каждой транзакции
2. test_transaction_description_generator тестирует функцию как генератор
3. test_transaction_description_with_empty_list работа функции с пустым списком
4. test_transaction_description_with_single_transaction работа функции с одной транзакцией
5. test_transaction_description_mix_transaction работа функции с разным количеством транзакций

## Тесты для card_number_generator

1. test_card_number_generator_basic тестирование базовой генерации номеров карт
2. test_card_number_generator_format тестирование формата номеров карт
3. test_card_number_generator_edge_cases тестирование граничных случаев
4. test_card_number_generator_invalid_start_greater_than_end 
Тестирование ошибки при начальном значении больше конечного
5. test_card_number_generator_invalid_end_too_large
Тестирование ошибки при слишком большом конечном значении
6. test_card_number_generator_invalid_start_too_small
Тестирование ошибки при слишком маленьком начальном значении


## Тесты для utils

1. test_read_transactions_from_json_valid_file
Тестирование чтения валидного JSON-файла с использованием моков
2. test_read_transactions_from_json_nonexistent_file
Тестирование чтения несуществующего файла
3. test_read_transactions_from_json_empty_file
Тестирование чтения пустого файла
4. test_read_transactions_from_json_invalid_json
Тестирование чтения невалидного JSON
5. test_read_transactions_from_json_non_list_content
Тестирование чтения файла, содержащего не список
6. test_read_transactions_from_json_with_spaces_in_keys
Тестирование очистки ключей и значений от пробелов (как в operations.json)
7. test_read_transactions_from_json_io_error
Тестирование обработки ошибки ввода-вывода
8. test_read_transactions_from_json_real_file
Тестирование чтения реального файла operations.json через фикстуру
9.  test_read_transactions_from_json_executed_count
Тестирование количества выполненных транзакций
10. test_read_transactions_from_json_canceled_count
Тестирование количества отменённых транзакций
11. test_read_transactions_from_json_usd_currency
Тестирование транзакций в валюте USD
12. test_read_transactions_from_json_rub_currency
Тестирование транзакций в валюте RUB
13. test_read_transactions_from_json_with_from_field
Тестирование транзакций с полем 'from'
14. test_read_transactions_from_json_without_from_field
Тестирование транзакций без поля 'from'
15. test_integration_read_real_operations_file
Интеграционный тест: чтение реального файла operations.json
16. test_integration_filter_usd_transactions
Интеграционный тест: фильтрация транзакций в USD после чтения
17. test_integration_get_transaction_descriptions
Интеграционный тест: получение описаний транзакций после чтения
18. test_read_transactions_from_json_large_file
Тестирование чтения большого файла (1000+ транзакций)
19. test_read_transactions_from_json_special_characters
Тестирование чтения файла со специальными символами
20. test_read_transactions_from_json_empty_list
Тестирование чтения файла с пустым списком

## Тесты и фикстуры для external_api

1. mock_env_vars
Фикстура для мокирования переменных окружения
2. sample_transaction_usd
Фикстура: транзакция в USD из operations.json
3. sample_transaction_rub
Фикстура: транзакция в RUB из operations.json
4. test_get_exchange_rate_success
Тестирование успешного получения курса валют
5. test_get_exchange_rate_api_error
Тестирование обработки ошибки API
6. test_get_exchange_rate_network_error
Тестирование обработки сетевой ошибки
7. test_get_exchange_rate_timeout
Тестирование обработки таймаута
8. test_get_exchange_rate_missing_api_key
Тестирование отсутствия API ключа
9. test_get_transaction_amount_in_rubles_usd
Тестирование получения суммы транзакции в рублях (USD)
10. test_get_transaction_amount_in_rubles_rub
Тестирование получения суммы транзакции в рублях (RUB)
11. test_get_transaction_amount_in_rubles_operationAmount_not_dict
Тестирование обработки случая, когда operationAmount не является словарём
12. test_get_transaction_amount_in_rubles_missing_operationAmount
Тестирование обработки транзакции без поля operationAmount
13. test_get_transaction_amount_in_rubles_missing_amount
Тестирование обработки транзакции без суммы
14. test_get_transaction_amount_in_rubles_missing_currency_code
Тестирование обработки транзакции без кода валюты
15. test_get_transaction_amount_in_rubles_with_spaces_in_keys
Тестирование обработки ключей с пробелами (как в operations.json)
16. test_convert_amount_to_rubles_rub
Тестирование конвертации суммы в рублях (без конвертации)
17. test_convert_amount_to_rubles_usd
Тестирование конвертации суммы из USD в рубли
18. test_convert_amount_to_rubles_eur
Тестирование конвертации суммы из EUR в рубли
19. test_convert_amount_to_rubles_rounding
Тестирование округления результата до 2 знаков
20. test_convert_amount_to_rubles_unsupported_currency
Тестирование конвертации неподдерживаемой валюты
21. test_convert_amount_to_rubles_rate_error
Тестирование обработки ошибки получения курса
22. test_integration_real_api
Интеграционный тест с реальным API


```bash
pytest 
```
### Документация

Более подробную документацию по каждой функции можно найти в `docstrings` и комментариях внутри исходного кода.

### Лицензия

Сведения о лицензии проекта (например, MIT, Apache 2.0) [укажите здесь](https://github.com).

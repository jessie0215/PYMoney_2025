# test_week12_all.py
#
# 這支程式會：
# - 用 DEFAULTCATEGORIES 測 Categories.view / find_subcategories / is_category_valid
# - 用測試版 Records 測 add / view / find / delete
# - 每個測試都印 [OK] or [FAIL]，讓你知道哪個功能正常、哪個需要修

import io
from contextlib import redirect_stdout
from unittest.mock import patch

import week12

# 為了不要動到你正式的檔案，我們可以改成測試版檔名
week12.RECORDSFILE = 'test_records.txt'
week12.CATEGORIESFILE = 'test_categories.txt'


# ----- 小工具：抓函式印出的所有東西 -----
def capture_output(func, *args, **kwargs):
    buf = io.StringIO()
    with redirect_stdout(buf):
        func(*args, **kwargs)
    return buf.getvalue()


def report_result(name, ok, extra_msg=""):
    if ok:
        print(f"[OK]   {name}")
    else:
        print(f"[FAIL] {name}")
        if extra_msg:
            print(extra_msg)
        print("-" * 40)


# ----- 測試用 Categories / Records -----

class TestCategories(week12.Categories):
    # 不讀檔，直接用 DEFAULTCATEGORIES
    def initialize_categories(self):
        self._categories = week12.DEFAULTCATEGORIES


class TestRecords(week12.Records):
    # 不讀檔、不問 initial money，直接給一個固定值
    @staticmethod
    def initialize():
        initial_money = 1000
        records = []
        return initial_money, records


# ----- 測試 Categories.view -----
def test_categories_view():
    cats = TestCategories()
    out = capture_output(cats.view)

    expected = (
        "- expense\n"
        "    - food\n"
        "        - meal\n"
        "        - snack\n"
        "        - drink\n"
        "    - transportation\n"
        "        - bus\n"
        "        - railway\n"
        "- income\n"
        "    - salary\n"
        "    - bonus\n"
    )

    ok = (out == expected)
    msg = f"expected:\n{repr(expected)}\n\ngot:\n{repr(out)}"
    report_result("Categories.view(DEFAULTCATEGORIES)", ok, msg if not ok else "")


# ----- 測試 Categories.find_subcategories -----
def test_find_subcategories():
    cats = TestCategories()

    cases = {
        'expense': [
            'expense', 'food', 'meal', 'snack', 'drink',
            'transportation', 'bus', 'railway'
        ],
        'food': ['food', 'meal', 'snack', 'drink'],
        'transportation': ['transportation', 'bus', 'railway'],
        'income': ['income', 'salary', 'bonus'],
        'salary': ['salary'],
        'bonus': ['bonus'],
        'nonexist': [],
    }

    all_ok = True
    for name, expected in cases.items():
        got = cats.find_subcategories(name)
        ok = (got == expected)
        if not ok:
            all_ok = False
            print(f"[FAIL] find_subcategories({name!r})")
            print(f"  expected: {expected}")
            print(f"  got     : {got}")
        else:
            print(f"[OK]   find_subcategories({name!r})")

    report_result("Categories.find_subcategories (all cases)", all_ok)


# ----- 測試 Categories.is_category_valid -----
def test_is_category_valid():
    cats = TestCategories()

    true_cases = ['expense', 'food', 'meal', 'snack',
                  'drink', 'transportation', 'bus',
                  'railway', 'income', 'salary', 'bonus']
    false_cases = ['abc', 'foo', 'income2', '']

    all_ok = True

    # 應該要 True 的
    for name in true_cases:
        if not cats.is_category_valid(name):
            all_ok = False
            print(f"[FAIL] is_category_valid({name!r}) -> expected True, got False")
        else:
            print(f"[OK]   is_category_valid({name!r}) == True")

    # 應該要 False 的
    for name in false_cases:
        if cats.is_category_valid(name):
            all_ok = False
            print(f"[FAIL] is_category_valid({name!r}) -> expected False, got True")
        else:
            print(f"[OK]   is_category_valid({name!r}) == False")

    report_result("Categories.is_category_valid", all_ok)


# ----- 測試 Records.add + view (mode=0) -----
def test_records_add_and_view():
    cats = TestCategories()
    recs = TestRecords()

    # 模擬使用者輸入三筆紀錄
    fake_input = "food lunch -100, drink coffee -50, salary job 30000"
    with patch('builtins.input', return_value=fake_input):
        recs.add(cats)

    # 應該成功加上三筆
    ok_len = (len(recs._records) == 3)
    if not ok_len:
        report_result("Records.add (length)", False,
                      f"expected 3 records, got {len(recs._records)}")
        return

    # 簡單檢查內容
    r1, r2, r3 = recs._records
    ok_content = (
        r1.category == 'food' and r1.description == 'lunch' and r1.amount == -100 and
        r2.category == 'drink' and r2.description == 'coffee' and r2.amount == -50 and
        r3.category == 'salary' and r3.description == 'job' and r3.amount == 30000
    )

    if not ok_content:
        msg = f"records content unexpected: {[ (r.category, r.description, r.amount) for r in recs._records]}"
        report_result("Records.add (content)", False, msg)
        return

    # 再測 view() 印出來的東西：只比對關鍵字
    out = capture_output(recs.view)
    # 應該包含 header、三筆紀錄的關鍵字、以及正確的 total
    expected_keywords = [
        "Here's your expense and income records:",
        "No.", "Category", "Description", "Amount",
        "food", "lunch", "-100",
        "drink", "coffee", "-50",
        "salary", "job", "30000",
        "Now you have",  # 總額提示
    ]
    ok_keywords = all(kw in out for kw in expected_keywords)

    # 依照初始 1000 + (-100) + (-50) + 30000
    expected_total = 1000 - 100 - 50 + 30000
    ok_total = (f"Now you have {expected_total} dollars." in out)

    ok = ok_len and ok_content and ok_keywords and ok_total
    msg = ""
    if not ok:
        msg = f"view() output:\n{out}"

    report_result("Records.add + Records.view(mode=0)", ok, msg)


# ----- 測試 Records.find (搭配 Categories.find_subcategories) -----
def test_records_find():
    cats = TestCategories()
    recs = TestRecords()

    # 先放幾筆紀錄
    recs._records = [
        week12.Record('food', 'lunch', -100),
        week12.Record('drink', 'coffee', -50),
        week12.Record('salary', 'job', 30000),
        week12.Record('transportation', 'bus', -40),
    ]

    # 找 food 底下的所有分類
    target = cats.find_subcategories('food')
    out = capture_output(recs.find, 'food', target)

    expected_keywords = [
        'Here\'s your expense and income records under category "food":',
        'food', 'lunch', '-100',
        'drink', 'coffee', '-50',
        # 不該出現 salary/job
        # 總額：-100 + (-50) = -150
        "The total amount above is -150."
    ]

    ok = all(kw in out for kw in expected_keywords) and ("salary" not in out and "job" not in out)
    msg = ""
    if not ok:
        msg = f"find() output:\n{out}"

    report_result("Records.find (with food subtree)", ok, msg)


# ----- 測試 Records.delete -----
def test_records_delete():
    cats = TestCategories()
    recs = TestRecords()

    # 先建三筆紀錄
    recs._records = [
        week12.Record('food', 'lunch', -100),
        week12.Record('drink', 'coffee', -50),
        week12.Record('salary', 'job', 30000),
    ]

    # delete() 裡面會先呼叫 view()，再問要刪哪一筆
    # 我們給使用者輸入 '2'，刪掉第二筆（drink coffee）
    with patch('builtins.input', return_value='2'):
        _ = capture_output(recs.delete)  # 把印出的東西吃掉就好

    ok_len = (len(recs._records) == 2)
    ok_order = (
        recs._records[0].category == 'food' and
        recs._records[1].category == 'salary'
    )

    ok = ok_len and ok_order
    msg = ""
    if not ok:
        msg = f"records after delete: {[ (r.category, r.description, r.amount) for r in recs._records]}"

    report_result("Records.delete (delete 2nd record)", ok, msg)


def main():
    print("===== TEST START =====\n")

    test_categories_view()
    print()
    test_find_subcategories()
    print()
    test_is_category_valid()
    print()
    test_records_add_and_view()
    print()
    test_records_find()
    print()
    test_records_delete()

    print("\n===== TEST END =====")


if __name__ == "__main__":
    main()

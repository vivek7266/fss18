import re as re
import traceback


class O:
    y = n = 0

    @staticmethod
    def report():
        print("\n# pass= %s fail= %s %%pass = %s%%" % (
            O.y, O.n, int(round(O.y * 100 / (O.y + O.n + 0.001)))))

    @staticmethod
    def k(f):
        try:
            print("\n-----| %s |-----------------------" % f.__name__)
            if f.__doc__:
                print("# " + re.sub(r'\n[ \t]*', "\n# ", f.__doc__))
            f()
            print("# pass")
            O.y += 1
        except:
            O.n += 1
            print(traceback.format_exc())
        return f


@O.k
def testingFailure():
    """this one must fail.. just to
    test if the  unit test system is working"""
    assert 1 == 2


@O.k
def testingSuccess():
    """if this one fails, we have a problem!"""
    assert 1 == 1


@O.k
def testing_whitespace_formatting():
    add_var = 1 + \
              2 + \
              3
    assert add_var == 6


@O.k
def testing_modules():
    """
    test import function
    """

    def regex_matcher(input):
        reg = re.compile("[0-9]")
        return reg.match(input).string

    assert regex_matcher("9") == "9"


@O.k
def testing_arithmetic():
    def divide(x, y):
        return x / y

    assert divide(11, 2) == 5.5


@O.k
def testing_functions():
    def incr_by_4(x):
        return x + 4

    def sum_and_increment_by_4(var_1, var_2):
        return incr_by_4(var_1 + var_2)

    assert sum_and_increment_by_4(2, 5) == 11


@O.k
def testing_strings():
    test_string_1 = "this is a one line"
    test_string_2 = 'this is a one line'

    assert len(test_string_1) == len(test_string_2)


@O.k
def testing_exceptions():
    def exception_function(x):
        try:
            var = 10 / x
        except ZeroDivisionError:
            return -1
        return var

    assert exception_function(0) == -1
    assert exception_function(10) == 1


@O.k
def testing_lists():
    def play_with_lists():
        l_1 = [1]
        l_1.append(2)
        l_1.extend([3, 4, 5])
        return l_1

    assert len(play_with_lists()) == 5
    assert play_with_lists()[:-1] == [1, 2, 3, 4]
    assert play_with_lists()[1:] == [2, 3, 4, 5]


@O.k
def testing_lists_2():
    def play_with_lists():
        l_1 = [1, 2]
        try:
            x, y, z = l_1
        except ValueError:
            return 0, 0, 0
        return x, y, z

    assert len(play_with_lists()) == 3


@O.k
def testing_tuples():
    def get_name_and_gender(inp_str):
        name_gender_split = inp_str.split(',')
        name = name_gender_split[0]
        gender = name_gender_split[1]
        return name, gender

    assert get_name_and_gender("vivek,male") == ("vivek", "male")


@O.k
def testing_dicts():
    courses = {"csc591": "fss", "csc512": "compiler", "csc522": "alda"}
    assert "csc591" in courses
    assert courses.get("csc591") == "fss"
    assert courses.get("csc592", "None") == "None"
    assert len(courses) == 3


@O.k
def testing_default_dicts():
    from collections import defaultdict

    courses = defaultdict(set)
    courses_tups = [("csc591", "fss"), ("csc512", "compiler"), ("csc522", "alda"), ("csc591", "fds")]
    for code, name in courses_tups:
        courses[code].add(name)
    assert "csc591" in courses
    assert courses.get("csc591") == {"fss", "fds"}
    assert courses.get("csc592", {}) == {}
    assert len(courses) == 3


@O.k
def testing_counter():
    from collections import Counter

    courses_tups = [("csc591", "fss"), ("csc512", "compiler"), ("csc522", "alda"), ("csc591", "fds")]
    most_common_code = Counter(code_name[0] for code_name in courses_tups).most_common(1)

    assert most_common_code == [("csc591", 2)]


@O.k
def testing_sets():
    course_codes = set()
    course_codes.add("csc591")
    course_codes.add("csc512")
    course_codes.add("csc522")
    course_codes.add("csc591")

    assert len(course_codes) == 3


@O.k
def testing_control_flow():
    def name_of_courses(code):
        course_names = []
        courses_tups = [("csc591", "fss"), ("csc512", "compiler"), ("csc522", "alda"), ("csc591", "fds")]

        for c, n in courses_tups:
            if code == c:
                course_names.append(n)
        return course_names

    assert name_of_courses("csc591") == ["fss", "fds"]
    assert name_of_courses("csc522") == ["alda"]


if __name__ == "__main__":
    O.report()

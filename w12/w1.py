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


@O.k
def testing_truthiness():
    def name_of_courses(code):
        course_names = []
        courses_tups = [("csc591", "fss"), ("csc512", "compiler"), ("csc522", "alda"), ("csc591", "fds")]

        for c, n in courses_tups:
            if code == c:
                course_names.append(n)
        return course_names

    assert not name_of_courses("csc519")
    assert not ""
    assert "csc591"
    assert not []
    assert [1, 2, 3]


@O.k
def testing_truthiness_any_all():
    assert not all([1, []])
    assert any([1, [], False])
    assert all([1, [2, 3], {4}, "5"])


@O.k
def testing_sorting():
    data = [0, -1, 2, 3, 4, 5, -6]

    data_sorted = sorted(data)
    data_sorted_abs = sorted(data, key=abs)
    data_sorted_abs_rev = sorted(data, key=abs, reverse=True)

    assert data_sorted[0] == -6
    assert data_sorted_abs[0] == 0
    assert data_sorted_abs_rev[0] == -6
    assert data_sorted_abs_rev[1] == 5


@O.k
def testing_list_comprehensions():
    data = [1, 2, 3, 4, 5, 6]
    even_odd = [0 if x % 2 == 0 else 1 for x in data]

    assert even_odd[::2] == [1, 1, 1]
    assert even_odd[1::2] == [0, 0, 0]


@O.k
def testing_generators_and_iterators():
    import sys

    def lazy_range(n):
        i = 0
        while i < n:
            yield i
        i += 1

    lazy_odd_number_generator = (i for i in range(100) if i % 2 != 0)
    lazy_odd_number_list = [i for i in range(100) if i % 2 != 0]

    assert not type(lazy_odd_number_generator) == type(lazy_odd_number_list)
    assert not sys.getsizeof(lazy_odd_number_generator) == sys.getsizeof(lazy_odd_number_list)


@O.k
def testing_randomness():
    import random

    random_data = []
    for i in range(2):
        random_data.append(random.randrange(10, 100))

    random_data_seeded = []
    for i in range(2):
        random.seed(5)
        random_data_seeded.append(random.randrange(10, 100))

    assert max(random_data) < 100
    assert min(random_data) > 10
    assert random_data_seeded[0] == random_data_seeded[1]


@O.k
def testing_regular_expressions():
    data = re.split("[v]", "vivek")

    assert re.search("v", "vivek")
    assert len(data) == 3
    assert data[2] == "ek"


@O.k
def testing_object_oriented_programming():
    class CourseName:

        def __init__(self, code="csc000", name="Unknown", full_name="Unknown"):
            self.code = code
            self.name = name
            self.full_name = full_name

        def __repr__(self):
            return ':'.join([self.code, self.name, self.full_name])

        def get_name(self):
            return self.name

        def get_code(self):
            return self.code

        def set_full_name(self, full_name):
            self.full_name = full_name

        def get_code_and_name(self):
            return self.code + " : " + self.name

    fss = CourseName("csc591", "fss")
    assert fss.full_name == "Unknown"

    fss_full_name = "foundations of software science"
    fss.set_full_name(fss_full_name)
    assert fss.full_name == fss_full_name


@O.k
def testing_functional_tools():
    from functools import partial

    def sum(x, y):
        return x + y

    def incr_by_4(x):
        return sum(4, x)

    incr_by_4_partial = partial(sum, 4)

    assert incr_by_4(5) == 9
    assert incr_by_4_partial(5) == 9


@O.k
def testing_map_reduce_filter():
    from functools import reduce

    data = [0, 1, 2, 3, 4]
    evened_data = map(lambda x: x - 1 if x % 2 != 0 else x, data)
    odded_data = map(lambda x: x - 1 if x % 2 == 0 else x, data)

    evened_data_gt_2 = filter(lambda x: x > 0, evened_data)
    odded_data_gt_3 = filter(lambda x: x > 0, odded_data)

    reduced_data_even = reduce(lambda x, y: x + y, evened_data_gt_2)
    reduced_data_odd = reduce(lambda x, y: x + y, odded_data_gt_3)

    assert reduced_data_even == reduced_data_odd


@O.k
def testing_enumerate():
    name = "foundations of software science"
    vocabulary = set(name)
    char_index = dict((c, i) for i, c in enumerate(vocabulary))
    assert len(char_index) == len(vocabulary)
    assert 'f' in char_index.keys() and 'f' in vocabulary


@O.k
def testing_zip_and_argument_unpacking():
    codes = ["csc591", "csc522", "csc512"]
    names = ["fss", "alda", "compiler"]

    code_name_pairs = list(zip(codes, names))
    code_name_unpacked = list(zip(*code_name_pairs))
    print(code_name_pairs)
    print(code_name_unpacked)

    assert code_name_pairs == [("csc591", "fss"), ("csc522", "alda"), ("csc512", "compiler")]
    assert code_name_unpacked == [('csc591', 'csc522', 'csc512'), ('fss', 'alda', 'compiler')]
    assert list(code_name_unpacked[0]) == codes
    assert list(code_name_unpacked[1]) == names


@O.k
def testing_args_kwargs():


if __name__ == "__main__":
    O.report()

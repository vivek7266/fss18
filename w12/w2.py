from testutils import O

DATA1 = """
outlook,$temp,?humidity,windy,play
sunny,85,85,FALSE,no
sunny,80,90,TRUE,no
overcast,83,86,FALSE,yes
rainy,70,96,FALSE,yes
rainy,68,80,FALSE,yes
rainy,65,70,TRUE,no
overcast,64,65,TRUE,yes
sunny,72,95,FALSE,no
sunny,69,70,FALSE,yes
rainy,75,80,FALSE,yes
sunny,75,70,TRUE,yes
overcast,100,25,90,TRUE,yes
overcast,81,75,FALSE,yes
rainy,71,91,TRUE,no"""

DATA2 = """
    outlook,   # weather forecast.
    $temp,     # degrees farenheit
    ?humidity, # relative humidity
    windy,     # wind is high
    play       # yes,no
    sunny,85,85,FALSE,no
    sunny,80,90,TRUE,no
    overcast,83,86,FALSE,yes

    rainy,70,96,FALSE,yes
    rainy,68,80,FALSE,yes
    rainy,65,70,TRUE,no
    overcast,64,

                  65,TRUE,yes
    sunny,72,95,FALSE,no
    sunny,69,70,FALSE,yes
    rainy,75,80,FALSE,yes
          sunny,
                75,70,TRUE,yes
    overcast,100,25,90,TRUE,yes
    overcast,81,75,FALSE,yes # unique day
    rainy,71,91,TRUE,no"""


def lines(s):
    """Return contents, one line at a time."""
    # yourCodeHere()
    return s.splitlines()


def rows(src):
    """Kill bad characters. If line ends in ','
     then join to next. Skip blank lines."""
    # yourCodeHere()
    data = []
    row_continued = ""
    for row in src:
        if row == "":
            continue
        if '#' in row:
            data_split = row.split('#')
            col_name = data_split[0].replace(' ', '')
        else:
            col_name = row.replace(' ', '')
        row_continued += col_name
        if col_name[-1] == ',':
            continue
        data.append(row_continued)
        row_continued = ""
    return data


def cols(src):
    """ If a column name on row1 contains '?',
    then skip over that column."""
    # yourCodeHere()
    result_data = []
    skip_indices = []
    headers = src[0]
    headers_split = headers.split(',')
    for i, c in enumerate(headers_split):
        if c[0] == '?':
            skip_indices.append(i)
    for row in src:
        row_data = []
        row_split = row.split(',')
        for i, v in enumerate(row_split):
            if i in skip_indices:
                continue
            else:
                row_data.append(v)
        result_data.append(row_data)
    return result_data


def prep(src):
    """ If a column name on row1 contains '$',
    coerce strings in that column to a float."""
    # yourCodeHere()
    result_data = []
    float_indices = []
    headers = src[0]
    result_data.append(headers)
    for i, c in enumerate(headers):
        if c[0] == '$':
            float_indices.append(i)
    for row in src[1:]:
        row_data = []
        for i, r in enumerate(row):
            if i in float_indices:
                row_data.append(float(r))
            else:
                row_data.append(r)
        result_data.append(row_data)
    return result_data


def ok0(s):
    for row in prep(cols(rows(lines(s)))):
        print(row)


# print(lines(DATA1))
# print(rows(lines(DATA1)))
# print(cols(rows(lines(DATA1))))
# print(prep(cols(rows(lines(DATA1)))))
#
# print(lines(DATA2))
# print(rows(lines(DATA2)))
# print(cols(rows(lines(DATA2))))
# print(prep(cols(rows(lines(DATA2)))))


@O.k
def ok1(): ok0(DATA1)


@O.k
def ok2(): ok0(DATA2)


if __name__ == "__main__":
    O.report()

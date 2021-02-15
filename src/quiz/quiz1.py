# ========================================================================
# Copyright 2021 Emory University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
import re
def normalize(text):
    cardinal = re.compile(
        r'(trillion|billion|million|thousand|hundred|ninety|eighty|seventy|sixty|fifty|fourty|thirty|twenty|nineteen|eighteen|seventeen|sixteen|fifteen|fourteen|thirteen|twelve|eleven|ten|nine|eight|seven|six|five|four|three|two|one|zero|trillionth|billionth|millionth|thousandth|hundredth|ninetieth|eightieth|seventieth|sixtieth|fiftieth|fortieth|thirtieth|twentieth|twelfth|ninth|eighth|fifth|third|second|first|zeroth)')
    ordinal = re.compile(
        r'(trillionth|billionth|millionth|thousandth|hundredth|ninetieth|eightieth|seventieth|sixtieth|fiftieth|fortieth|thirtieth|twentieth|twelfth|ninth|eighth|fifth|third|second|first|zeroth)')
    point = re.compile(r'(point)')

    nt = text
    lt = nt.lower()
    si = 0
    ei = 0
    new = -1
    num3 = 0
    num2 = 0
    num1 = 0
    overlap1 = 0
    overlap2 = 0
    isdecimal = False
    pp = point.finditer(lt)
    prev = 0
    rt = ''
    for m in cardinal.finditer(lt):
        if new == -1:
            si = m.start()
            ei = m.end()
            new = 0
        else:
            if lt[ei:m.start()] not in {' ', '-'}:
                if (nt[ei:ei + 6]) in {' point'} and (nt[m.start() - 6:m.start()]) in {'point '}:
                    isdecimal = True
                    num1 = 0
                    num2 = 0
                    si = m.start()
                    ei = m.end()
                    overlap1 = 0
                    overlap2 = 0
                    new = 0
                elif isdecimal == True:
                    isdecimal = False
                    num1 = 0
                    num2 = 0
                    si = m.start()
                    ei = m.end()
                    new = 0
                    overlap1 = 0
                    overlap2 = 0
                else:
                    num2 += num1
                    rt = rt + nt[prev:si] + str(num2)
                    prev = ei
                    num1 = 0
                    num2 = 0
                    si = m.start()
                    ei = m.end()
                    new = 0
                    overlap1 = 0
                    overlap2 = 0
        n = lt[m.start():m.end()]
        if n in {'trillion', 'billion', 'million', 'thousand', 'hundred'}:
            if m.start() > 1 and m.start() == si:
                if nt[m.start() - 2: m.start()] in {'a '}:
                    si = m.start() - 2
                    num1 = 1
            if num1 == 0: num1 = 1
            if n in {'trillion'}:
                num1 = num1 * 1000000000000
                num2 += num1
                num1 = 0
            elif n in {'billion'}:
                num1 = num1 * 1000000000
                num2 += num1
                num1 = 0
            elif n in {'million'}:
                num1 = num1 * 1000000
                num2 += num1
                num1 = 0
            elif n in {'thousand'}:
                num1 = num1 * 1000
                num2 += num1
                num1 = 0
            elif n in {'hundred'}:
                num1 = num1 * 100
                overlap1 = 0
                overlap2 = 0
        else:
            if num1 == 0:
                overlap1 = 0
                overlap2 = 0
            num3 = convert(n)
            if num3 > 9 and overlap2 == 1:
                new = -1
            elif num3 > 9:
                overlap2 = 1
            if num3 < 20 and overlap1 == 1:
                new = -1
            elif num3 < 20:
                overlap1 = 1
            if new == -1:
                if isdecimal != True:
                    num2 += num1
                    rt = rt + nt[prev:si] + str(num2)
                    prev = ei
                num1 = 0
                num2 = 0
                si = m.start()
                ei = m.end()
                new = 0
            num1 += num3

        ei = m.end()
        for o in ordinal.finditer(lt):
            if m.start() == o.start():
                new = -1
                num2 = 0
                num1 = 0

    if isdecimal == True:
        rt = rt + nt[prev:]
    elif new != -1:
        num2 += num1
        rt = rt + nt[prev:si] + str(num2) + nt[ei:]
    return rt

def convert(n):
    result = 0
    if n in {'trillion'}:
        result = 1000000000000
    if n in {'billion'}:
        result = 1000000000
    if n in {'million'}:
        result = 1000000
    if n in {'thousand'}:
        result = 1000
    if n in {'hundred'}:
        result = 100
    if n in {'ninety'}:
        result = 90
    if n in {'eighty'}:
        result = 80
    if n in {'seventy'}:
        result = 70
    if n in {'sixty'}:
        result = 60
    if n in {'fifty'}:
        result = 50
    if n in {'fourty'}:
        result = 40
    if n in {'thirty'}:
        result = 30
    if n in {'twenty'}:
        result = 20
    if n in {'nineteen'}:
        result = 19
    if n in {'eighteen'}:
        result = 18
    if n in {'seventeen'}:
        result = 17
    if n in {'sixteen'}:
        result = 16
    if n in {'fifteen'}:
        result = 15
    if n in {'fourteen'}:
        result = 14
    if n in {'thirteen'}:
        result = 13
    if n in {'twelve'}:
        result = 12
    if n in {'eleven'}:
        result = 11
    if n in {'ten'}:
        result = 10
    if n in {'nine'}:
        result = 9
    if n in {'eight'}:
        result = 8
    if n in {'seven'}:
        result = 7
    if n in {'six'}:
        result = 6
    if n in {'five'}:
        result = 5
    if n in {'four'}:
        result = 4
    if n in {'three'}:
        result = 3
    if n in {'two'}:
        result = 2
    if n in {'one'}:
        result = 1
    if n in {'zero'}:
        result = 0
    return result

def normalize_extra(text):
    # TODO: to be updated
    return text


if __name__ == '__main__':
    S = [
        'I met twelve people',
        'I have one brother and two sisters',
        'A year has three hundred sixty five days',
        'I made a million dollars'
    ]

    T = [
        'I met 12 people',
        'I have 1 brother and 2 sisters',
        'A year has 365 days',
        'I made 1000000 dollars'
    ]

    correct = 0
    for s, t in zip(S, T):
        if normalize(s) == t:
            correct += 1

    print('Score: {}/{}'.format(correct, len(S)))
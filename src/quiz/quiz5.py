# ========================================================================
# Copyright 2020 Emory University
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
import glob
import os
from types import SimpleNamespace
from typing import Iterable, Tuple, Any, List, Set

import ahocorasick


def create_ac(data: Iterable[Tuple[str, Any]]) -> ahocorasick.Automaton:
    """
    Creates the Aho-Corasick automation and adds all (span, value) pairs in the data and finalizes this matcher.
    :param data: a collection of (span, value) pairs.
    """
    AC = ahocorasick.Automaton(ahocorasick.STORE_ANY)

    for span, value in data:
        if span in AC:
            t = AC.get(span)
        else:
            t = SimpleNamespace(span=span, values=set())
            AC.add_word(span, t)
        t.values.add(value)

    AC.make_automaton()
    return AC


def read_gazetteers(dirname: str) -> ahocorasick.Automaton:
    data = []
    for filename in glob.glob(os.path.join(dirname, '*.txt')):
        label = os.path.basename(filename)[:-4]
        for line in open(filename):
            data.append((line.strip(), label))
    return create_ac(data)


def match(AC: ahocorasick.Automaton, tokens: List[str]) -> List[Tuple[str, int, int, Set[str]]]:
    """
    :param AC: the finalized Aho-Corasick automation.
    :param tokens: the list of input tokens.
    :return: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a set of values for the span: Set[str]
    """
    smap, emap, idx = dict(), dict(), 0
    for i, token in enumerate(tokens):
        smap[idx] = i
        idx += len(token)
        emap[idx] = i
        idx += 1

    # find matches
    text = ' '.join(tokens)
    spans = []
    for eidx, t in AC.iter(text):
        eidx += 1
        sidx = eidx - len(t.span)
        sidx = smap.get(sidx, None)
        eidx = emap.get(eidx, None)
        if sidx is None or eidx is None: continue
        spans.append((t.span, sidx, eidx + 1, t.values))

    return spans


def remove_overlaps(entities: List[Tuple[str, int, int, Set[str]]]) -> List[Tuple[str, int, int, Set[str]]]:
    """
    :param entities: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a set of values for the span: Set[str]
    :return: a list of entities where each entity is represented by a tuple of (span, start index, end index, value set)
    """
    # TODO: to be updated
    if len(entities) == 0:
        return entities

    s = 0
    e = entities[0][2]
    totals = 0
    totale = entities[0][2]

    i = 1
    total = []
    result = []
    total.append(entities[0])
    tmp = []
    tmp.append(entities[0])
    while i < len(entities):
        if entities[i][1] >= totale:
            j = len(total) - 1
            k = len(tmp) - 1
            ns = entities[i][1]
            while k >= 0:
                if j > 0:
                    pe = total[j - 1][2]
                else:
                    pe = totals
                if j < len(total) - 1:
                    ns = total[j + 1][1]

                if tmp[k][1] >= pe and tmp[k][2] <= ns:
                    if tmp[k][2] - tmp[k][1] > total[j][2] - total[j][1]:
                        total[j] = tmp[k]
                if tmp[k][1] < pe:
                    j = j - 1
                    continue
                k = k - 1
            result.extend(total)
            total = []
            tmp = []
            s = entities[i][1]
            e = entities[i][2]
            totals = entities[i][1]
            totale = entities[i][2]
            total.append(entities[i])

        elif entities[i][1] >= e:
            total.append(entities[i])
            s = e
            e = entities[i][2]
            totale = entities[i][2]
        elif entities[i][2] < e and entities[i][1] >= s:
            total.pop()
            total.append(entities[i])
            e = entities[i][2]
        else:
            if entities[i][2] > totale:
                totale = entities[i][2]
        tmp.append(entities[i])
        i = i + 1
    if tmp:
        j = len(total) - 1
        k = len(tmp) - 1
        ns = totale

        while k >= 0:
            if j > 0:
                pe = total[j - 1][2]
            else:
                pe = totals
            if j < len(total) - 1:
                ns = total[j + 1][1]

            if tmp[k][1] >= pe and tmp[k][2] <= ns:
                if tmp[k][2] - tmp[k][1] > total[j][2] - total[j][1]:
                    total[j] = tmp[k]
            if tmp[k][1] < pe:
                j = j - 1;
                continue
            k = k - 1;
        result.extend(total)
    return result


def to_bilou(tokens: List[str], entities: List[Tuple[str, int, int, str]]) -> List[str]:
    """
    :param tokens: a list of tokens.
    :param entities: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a named entity tag
    :return: a list of named entity tags in the BILOU notation with respect to the tokens
    """
    # TODO: to be updated
    result = tokens[:]
    for i in range(len(result)):
        result[i] = 'O'
    for e in entities:
        for i in range(e[1], e[2]):
            if i == e[1] and i + 1 == e[2]:
                result[i] = 'U-' + e[3]
            elif i == e[1]:
                result[i] = 'B-' + e[3]
            elif i == e[2] - 1:
                result[i] = 'L-' + e[3]
            else:
                result[i] = 'I-' + e[3]
    return result


if __name__ == '__main__':
    gaz_dir = 'dat/ner'
    AC = read_gazetteers('dat/ner')

    tokens = 'Atlantic City of Georgia'.split()
    entities = match(AC, tokens)
    entities = remove_overlaps(entities)
    print(entities)
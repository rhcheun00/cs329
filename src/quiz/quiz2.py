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
from typing import Set, Optional, List
from nltk.corpus.reader import Synset
from nltk.corpus import wordnet as wn


def antonyms(sense: str) -> Set[Synset]:
    """
    :param sense: the ID of the sense (e.g., 'dog.n.01').
    :return: a set of Synsets representing the union of all antonyms of the sense as well as its synonyms.
    """
    # TODO: to be updated
    sense0 = wn.synset(sense)
    lem = []
    result = set()
    for l in sense0.lemmas():
        for x in l.antonyms():
            lem.append(x)
    for l in lem:
        result.add(l.synset())
    return result


def paths(sense_0: str, sense_1: str) -> List[List[Synset]]:
    # TODO: to be updated
    synset_0 = wn.synset(sense_0)
    synset_1 = wn.synset(sense_1)
    hypernym_paths_0 = synset_0.hypernym_paths()
    hypernym_paths_1 = synset_1.hypernym_paths()
    lch = synset_0.lowest_common_hypernyms(synset_1)
    result = []
    for hypernym in lch:
        path0 = []
        path1 = []

        for syn_list0 in hypernym_paths_0:
            paths = []
            l0 = len(syn_list0) - 1
            tf = True
            while l0 >= 0:
                paths.append(syn_list0[l0])
                if (syn_list0[l0] == hypernym):
                    for p in path0:
                        if p == paths:
                            tf = False
                    if tf:
                        path0.append(paths)
                    break
                l0 = l0 - 1
        for syn_list1 in hypernym_paths_1:
            paths = []
            l1 = len(syn_list1) - 1
            tf = True
            while l1 >= 0:
                if (syn_list1[l1] == hypernym):
                    for p in path1:
                        if p == paths:
                            tf = False
                    if tf:
                        path1.append(paths)
                    break
                paths.append(syn_list1[l1])
                l1 = l1 - 1

        for p0 in path0:
            for p1 in path1:
                p1.reverse()
                p2 = p0 + p1
                result.append(p2)
    if result == []:
        return [[]]
    return result


if __name__ == '__main__':
    print(antonyms('purchase.v.01'))

    for path in paths('dog.n.01', 'cat.n.01'):
        print([s.name() for s in path])
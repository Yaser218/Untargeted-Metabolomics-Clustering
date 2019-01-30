#!/usr/bin/env python2
#encoding: UTF-8
"""
    The cosine class will calculate and return the similarity
    between two given mass spectrum.
    @author: Yaser Alkhalifah, Jan - 2019
"""
from math import sqrt

class Cosine:

    def __init__(self, dataset):
        self.dataset = dataset

    def cosine_similarity(self, mass_a, mass_b):
        """
            Calculate the cosine similarity between 2 given VOCs.
        """
        numerator = sum(a * b for a, b in zip(mass_a, mass_b))
        denominator = self.square_rooted(mass_a) * self.square_rooted(mass_b)
        return round(numerator/float(denominator), 3)

    def square_rooted(self, mass):
        """
            Calculate the square root for a VOC's mass.
        """
        return round(sqrt(sum([a * a for a in mass])), 3)

    def normalisation(self, voc_index):
        """
           Extract the EIC for particular VOC,
           and normalise all m/z intensities based on the EIC intense value.
        """
        extracted_normalisation = []
        max_ints = max(self.dataset[voc_index][3:])
        for Int in range(3, len(self.dataset[voc_index])):
            extracted_normalisation.append((self.dataset[voc_index][Int] / max_ints))
        return extracted_normalisation

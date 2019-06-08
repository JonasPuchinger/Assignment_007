#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys

# Original operators
KLM_K = 0.28
KLM_P = 1.10
KLM_B = 0.10
KLM_M = 1.20
KLM_H = 0.40

# Our operators. Adjust accordingly if necessary
CUSTOM_K = 0.33
CUSTOM_P = 0.76
CUSTOM_B = 0.09
CUSTOM_H = 0.56


class KLM:

    def __init__(self, filename):
        self.amount_k = 0
        self.amount_p = 0
        self.amount_b = 0
        self.amount_m = 0
        self.amount_h = 0
        if self.read_file(filename):
            self.calculate_predictions()

    def read_file(self, filename):
        #print('Reading ' + str(filename))
        try:
            file = open(filename)
            readline = file.readlines()
            multiplier = 1
            number = ''
            read_number = False
            # Read every line
            for line in readline:
                #print(line)
                # Read every char in current line
                for char in line:
                    #print(char)
                    # Check if current char is a number
                    if char.lower().isdigit():
                        # If the iteration before char was a number combine char to one number
                        if read_number:
                            number += char
                            multiplier = int(number)
                        else:
                            number = char
                            multiplier = int(char)
                        read_number = True
                        #print('multiplier: ' + str(multiplier) + ' Number: ' + number)
                    elif char.lower() == 'k':
                        self.amount_k += multiplier
                        multiplier = 1
                        read_number = False
                    elif char.lower() == 'p':
                        self.amount_p += multiplier
                        multiplier = 1
                        read_number = False
                    elif char.lower() == 'b':
                        self.amount_b += multiplier
                        multiplier = 1
                        read_number = False
                    elif char.lower() == 'm':
                        self.amount_m += multiplier
                        multiplier = 1
                        read_number = False
                    elif char.lower() == 'h':
                        self.amount_h += multiplier
                        multiplier = 1
                        read_number = False
                    else:
                        multiplier = 1
                        read_number = False
                        break
            return True
        except FileNotFoundError:
            print('Failed to open file!')
            return False

    # Calculate predictions
    def calculate_predictions(self):
        print('K: {0} P: {1} B: {2} M: {3} H: {4}'.format(self.amount_k, self.amount_p, self.amount_b, self.amount_m, self.amount_h))
        original_prediction = self.amount_k * KLM_K + \
            self.amount_p * KLM_P + \
            self.amount_b * KLM_B + \
            self.amount_m * KLM_M + \
            self.amount_h * KLM_H
        custom_prediction = self.amount_k * CUSTOM_K + \
            self.amount_p * CUSTOM_P + \
            self.amount_b * CUSTOM_B + \
            self.amount_m * KLM_M + \
            self.amount_h * CUSTOM_H

        print('Prediction using original KLM: ' + str(round(original_prediction, 2)) + 's')
        print('Prediction using custom values: ' + str(round(custom_prediction, 2)) + 's')


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Filename is missing. Usage: %s <file>\n" % sys.argv[0])
    else:
        klm = KLM(sys.argv[1])


if __name__ == '__main__':
    main()

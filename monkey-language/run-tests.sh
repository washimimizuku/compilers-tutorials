#!/bin/sh

coverage run --omit '*/_virtualenv.py' -m unittest discover && coverage report -m

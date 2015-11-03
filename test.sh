#!/bin/bash

coverage run --source='softdelete' runtests.py
coverage annotate -d coverage_annotate
coverage report

"""
The flask application package.
"""
# -*- coding: latin-1 -*-
from flask import Flask
app = Flask(__name__)

import PersonalPage.views

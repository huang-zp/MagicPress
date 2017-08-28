# -*- coding: utf-8 -*-
import tinify
from flask import current_app


def ting_pic(filename, savename):
    try:
        tinify.key = "******"
        tinify.validate()
    except tinify.Error, e:
        # Validation of API key failed.
        current_app.logger.error(tinify.Error)
        current_app.logger.error(e)
    try:
        source = tinify.from_file(filename)
    except Exception as e:
        source.to_file(filename)
        current_app.logger.error(e)
    source.to_file(savename)

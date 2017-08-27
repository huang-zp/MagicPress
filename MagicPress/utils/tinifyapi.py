# -*- coding: utf-8 -*-
import tinify

def ting_pic(filename, savename):
    try:
        tinify.key = "******"
        tinify.validate()
    except tinify.Error, e:
        # Validation of API key failed.
        pass
    try:
        source = tinify.from_file(filename)
    except:
        source.to_file(filename)
    source.to_file(savename)
import pytest
import imp
import json
import os

module_path = os.path.abspath('../cloudpassage')

file, filename, data = imp.find_module('exceptions', [module_path])
exceptions = imp.load_module('exceptions', file, filename, data)
file, filename, data = imp.find_module('fn', [module_path])
fn = imp.load_module('fn', file, filename, data)


class TestFn:
    def test_merge_dicts(self):
        one = {"a": "Alpha",
               "b": "Bravo",
               "c": "Charlie"}
        two = {"c": "CharlieHorse",
               "d": "Delta",
               "e": "Echo"}
        merge_one = fn.merge_dicts(one, two)
        merge_two = fn.merge_dicts(two, one)
        assert merge_one["c"] == "CharlieHorse"
        assert merge_two["c"] == "Charlie"

    def test_parse_status200(self):
        resp_text = "Test text, yo."
        url = "https://whatever.notevenpayingattention.because/its-not-critical"
        code_exc = {200: None,
                    201: None,
                    202: None,
                    204: None,
                    400: exceptions.CloudPassageValidation(resp_text),
                    401: exceptions.CloudPassageAuthentication(resp_text),
                    403: exceptions.CloudPassageAuthorization(resp_text),
                    404: exceptions.CloudPassageResourceExistence(resp_text),
                    422: exceptions.CloudPassageValidation(resp_text),
                    999999: exceptions.CloudPassageGeneral(resp_text)}
        code_succ = {200: True,
                     201: True,
                     202: True,
                     204: True,
                     400: False,
                     401: False,
                     403: False,
                     404: False,
                     422: False,
                     "ARBLEGARBLE" : False}
        for r, o in code_exc.items():
            success, exc = fn.parse_status(url, r, resp_text)
            assert type(o) == type(exc)
        for r, o in code_succ.items():
            success, exc = fn.parse_status(url, r, resp_text)
            assert success == o

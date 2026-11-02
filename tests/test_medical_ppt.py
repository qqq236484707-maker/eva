import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("medical_ppt",ROOT/"tools/medical_ppt.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class MedicalDeckTests(unittest.TestCase):
    def test_three_course_schemas(self):
        for name in ("aki","cvc","crrt"):
            p=ROOT/"courses"/name/"deck.json"
            deck=mod.load(p)
            self.assertEqual(deck["course_id"],name)
            self.assertEqual(len(deck["slides"]),5)
    def test_build_and_check(self):
        with tempfile.TemporaryDirectory() as td:
            for name in ("aki","cvc","crrt"):
                p=ROOT/"courses"/name/"deck.json"
                out=Path(td)/(name+".pptx")
                mod.build(p,out)
                result=mod.check(out,p)
                self.assertTrue(result["ok"],result)
                self.assertEqual(result["slides"],5)
    def test_draft_cannot_release(self):
        with self.assertRaises(ValueError):
            mod.load(ROOT/"courses/aki/deck.json",True)
    def test_missing_reference_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            d=mod.load(ROOT/"courses/aki/deck.json")
            d["slides"][2]["source_ids"]=["NOT_FOUND"]
            p=Path(td)/"deck.json"
            p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError): mod.load(p)
    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            d=mod.load(ROOT/"courses/aki/deck.json")
            d["assets"]={"A1":{"path":"../outside.png","kind":"image","license":"test","source":"test","alt":"test"}}
            p=Path(td)/"deck.json"
            p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError): mod.load(p)
if __name__=="__main__": unittest.main()

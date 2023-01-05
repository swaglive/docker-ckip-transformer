# -*- coding: utf-8 -*-
import os

from flask import Flask, request
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker


class Config:
  CKIP_DEVICE = os.environ.get('CKIP_DEVICE') or -1 
  CKIP_TRANSFORMER_MODEL = os.environ.get('CKIP_TRANSFORMER_MODEL') or 'bert-base'

app = Flask(__name__)
app.config.from_object(Config())

ws_driver, pos_driver, ner_driver = [
  driver(
    device=app.config['CKIP_DEVICE'], 
    model=app.config['CKIP_TRANSFORMER_MODEL'],
  ) for driver in [CkipWordSegmenter, CkipPosTagger, CkipNerChunker]
]

@app.route('/tokenize', methods=['GET'], endpoint='tokenize')
def tokenize():
  tokens = ws_driver(request.args.getlist('text'))
  return {'tokens': tokens}

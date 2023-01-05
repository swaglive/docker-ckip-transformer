# -*- coding: utf-8 -*-
import os

from flask import Flask, request, current_app
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker


app = Flask(__name__)
app.config |= {
    'CKIP_DEVICE': os.environ.get('CKIP_DEVICE') or -1,
    'CKIP_TRANSFORMER_MODEL': os.environ.get('CKIP_TRANSFORMER_MODEL') or 'bert-base',
}
app.config |= {
    'CKIP_DRIVERS': {
        name: Cls(
            device=app.config['CKIP_DEVICE'], 
            model=app.config['CKIP_TRANSFORMER_MODEL'],
        ) for name, Cls in {
            'ws': CkipWordSegmenter,
            'pos': CkipPosTagger,
            'ner': CkipNerChunker,
        }.items()
    },
}


@app.route('/tokenize', methods=['GET'], endpoint='tokenize')
def tokenize():
    return {
        'tokens': current_app.config['CKIP_DRIVERS']['ws'](
            request.args.getlist('text'),
        ),
    }

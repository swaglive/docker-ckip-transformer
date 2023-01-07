# -*- coding: utf-8 -*-
import os

from flask import Flask, request, current_app, Response
from ckip_transformers.nlp import CkipWordSegmenter


app = Flask(__name__)

@app.cli.command('touch')
def touch():
    """
    Initialize app and load model.
    """
    pass

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
        }.items()
    },
}


@app.route('/healthz', methods=['GET'], endpoint='healthz')
def healthz():
    return Response()


@app.route('/tokenize', methods=['GET'], endpoint='tokenize')
def tokenize():
    return {
        'tokens': current_app.config['CKIP_DRIVERS']['ws'](
            input_text=request.args.getlist('text'),
            show_progress=False,
        ),
    }

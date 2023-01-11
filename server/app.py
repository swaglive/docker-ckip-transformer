# -*- coding: utf-8 -*-
import os

from flask import Flask, request, current_app, Response

from . import drivers


app = Flask(__name__)
app.config |= {
    'CKIP_DEVICE': int(os.environ.get('CKIP_DEVICE') or -1),
    'CKIP_TRANSFORMER_MODEL': os.environ.get('CKIP_TRANSFORMER_MODEL') or 'bert-base',
}
app.config |= {
    'CKIP_DRIVERS': {
        name: Cls(
            device=app.config['CKIP_DEVICE'], 
            model=app.config['CKIP_TRANSFORMER_MODEL'],
        ) for name, Cls in {
            'ws': drivers.CkipWordSegmenter,
        }.items()
    },
}


@app.cli.command('touch')
def touch():
    pass


@app.route('/healthz', methods=['GET'], endpoint='healthz')
def healthz():
    return Response()


@app.route('/tokenize', methods=['GET'], endpoint='tokenize')
def tokenize():
    tokens = []

    if input_text := request.args.getlist('text'):
        tokens = current_app.config['CKIP_DRIVERS']['ws'](
            input_text=input_text,
            show_progress=False,
        )

    return {'tokens': tokens}

from flask import Blueprint, render_template, jsonify, app

from edinet import edinet_methods
from eve_docs.config import get_cfg


def edinet_docs():
    blueprints = [edinet_methods.edinet_methods]
    eve_docs = Blueprint('eve_docs', __name__,
                        template_folder='templates')

    @eve_docs.route('/')
    def index():
        cfg = get_cfg(blueprints)
        return render_template('index.html', cfg=cfg)

    @eve_docs.route('/v1/docs')
    def indexv1():
        cfg = get_cfg(blueprints)
        return render_template('indexv1.html', cfg=cfg)

    @eve_docs.route('/v1/spec.json')
    def spec():
        cfg = get_cfg(blueprints)
        return jsonify(cfg)

    return eve_docs

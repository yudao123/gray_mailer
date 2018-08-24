# coding=utf-8

import os
import json
import traceback
from flask import Blueprint, jsonify, request
from flask import render_template
from flu import build_app, load_config, conf

import send_email

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'template')

api = Blueprint('main', __name__, template_folder=TEMPLATE_DIR)


@api.route('/webhook')
def webhook_explain():
    return '<h1>This is a WebHook</h1>'

@api.route('/webhook', methods = ['POST'])
def webhook():
    raw_data = request.get_data()
    try:
        if raw_data:
            data = json.loads(raw_data)
        else:
            data = {}
    except:
        print('bad raw data, not json :', raw_data)
        traceback.print_exc()
        data = {}
    title = data.get('stream', {}).get('title', 'Graylog Alert')
    title = '告警：{}'.format(title)
    try:
        content = render_template('index.html', **data)
        send_email.send_email(title, content, [])
        return jsonify({'status': 'ok'})
    except:
        traceback.print_exc()
        return jsonify({'status': 'err'})

def initialize():

    load_config([
        ('FLU_CONFIG_FILE', 'config.yaml'),
        ('SMTP_LOGIN', ''),
        ('SMTP_PASSWORD', ''),
        ('EMAIL_RECEIVERS', ''),
        ('SMTP_HOST', 'smtp.partner.outlook.cn'),
        ('SMTP_PORT', 587),
        ('SMTP_MODE', 'tls'),
    ])

    if not conf.EMAIL_RECEIVERS:
        conf.put_config('EMAIL_RECEIVERS', conf.SMTP_LOGIN)

    conf.put_config('SMTP_PORT', int(conf.SMTP_PORT))

initialize()

module = type('CoreModule', (), {'route_map':[('/', api)]})

app = build_app([module])

if __name__ == '__main__':

    app.run(port=8000)






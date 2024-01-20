from libs.bot import Bot
from flask import Flask, request, jsonify
from markupsafe import escape
import argparse
import os
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='path to the configuration file')

    args = parser.parse_args()
    config_path = os.path.realpath(args.config) if args.config else (
        os.path.join(os.path.split(os.path.realpath(__file__))[0], 'config.json'))
    print(f"Configuration file path: {config_path}")

    with open(config_path) as f:
        config = json.loads(f.read())

    bot = Bot(
        session_token=config['ChatGPT']['session_token'],
        conversation_id=config['ChatGPT']['conversation_id'],
        proxy=config['ChatGPT']['proxy'],
        chrome_args=config['ChatGPT']['chrome_args'],
        disable_moderation=config['ChatGPT']['disable_moderation'],
        verbose=config['ChatGPT']['verbose'],
        headless=config['ChatGPT']['headless']
    )

    app = Flask(__name__)

    @app.route('/send_message', methods=['POST'])
    def send_message():
        response = {'status': {'failed': False, 'exception': ''}, 'message': ''}
        try:
            data = request.get_json()
            input_message = escape(data['message'])

            bot.new_chat()
            output_message = bot.send_message(input_message,
                                              input_mode=config['ChatGPT']['send_message']['input_mode'],
                                              input_delay=config['ChatGPT']['send_message']['input_delay'],
                                              timeout=config['ChatGPT']['send_message']['timeout'])

            if output_message.failed:
                response['status']['failed'] = True
            else:
                response['message'] = output_message.response
            return jsonify(response)

        except Exception as e:
            response['status']['failed'] = True
            response['status']['exception'] = str(e)
            return jsonify(response)

    app.run()


if __name__ == '__main__':
    main()

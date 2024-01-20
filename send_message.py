from libs.bot import Bot
import argparse


def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--message', help='Specify the message')
    group.add_argument('--message_file', help='Specify the file containing the message')

    parser.add_argument('--session_token', required=True,
                        help='The session token for authentication. (required)')
    parser.add_argument('--conversation_id', default='',
                        help='The conversation ID. Defaults to \'\'.')

    parser.add_argument('--proxy', default=None, help='The proxy server URL. Defaults to None.')
    parser.add_argument('--chrome_args', default=None, help='Chrome arguments')
    parser.add_argument('--disable_moderation', action='store_true',
                        help='Whether to disable moderation. Defaults to False.')
    parser.add_argument('--verbose', action='store_true',
                        help='Whether to enable verbose logging. Defaults to False.')
    parser.add_argument('--headless', action='store_true',
                        help='Whether to run the browser in headless mode. Defaults to False.')

    parser.add_argument('--input_mode', default='INSTANT', help='The input mode. Defaults to \'INSTANT\'.')
    parser.add_argument('--input_delay', type=float, default=0.1, help='The input delay. Defaults to 0.1.')
    parser.add_argument('--timeout', type=int, default=240, help='Timeout in seconds. Defaults to 240.')

    parser.add_argument('--output_file', default=None,
                        help='Specify the output file path, or it will be printed to console')

    args = parser.parse_args()
    if args.message:
        input_message = args.message
    elif args.message_file:
        with open(args.message_file, 'r', encoding='utf-8') as f:
            input_message = f.read()

    bot = Bot(
        session_token=args.session_token,
        conversation_id=args.conversation_id,
        proxy=args.proxy,
        chrome_args=args.chrome_args,
        disable_moderation=args.disable_moderation,
        verbose=args.verbose,
        headless=args.headless
    )

    bot.new_chat()
    output_message = bot.send_message(input_message,
                                      input_mode=args.input_mode,
                                      input_delay=args.input_delay,
                                      timeout=args.timeout)

    if output_message.failed:
        raise Exception("UnlimitedGPT Failed")
    else:
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output_message.response)
        else:
            print(output_message.response)


if __name__ == '__main__':
    main()

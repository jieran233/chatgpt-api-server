from libs.bot import Bot
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--message', required=True, help='Message (required)')
    parser.add_argument('--session_token', required=True, help='Session token (required)')
    parser.add_argument('--conversation_id', required=True, help='Conversation ID (required)')

    parser.add_argument('--proxy', default=None, help='Proxy setting')
    parser.add_argument('--chrome_args', default=None, help='Chrome arguments')
    parser.add_argument('--disable_moderation', action='store_true', help='Disable moderation')
    parser.add_argument('--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('--input_mode', default='INSTANT', help='Input mode')
    parser.add_argument('--input_delay', type=float, default=0.1, help='Input delay')

    args = parser.parse_args()

    bot = Bot(
        session_token=args.session_token,
        conversation_id=args.conversation_id,
        proxy=args.proxy,
        chrome_args=args.chrome_args,
        disable_moderation=args.disable_moderation,
        verbose=args.verbose,
    )

    bot.new_chat()
    output_message = bot.send_message(args.message, input_mode=args.input_mode, input_delay=args.input_delay)

    if output_message.failed:
        raise Exception("UnlimitedGPT Failed")
    else:
        print(output_message.response)


if __name__ == '__main__':
    main()

from mattermostdriver import Driver
import argparse

auth_info = {'url': 'mattermost.domain.url',
             'login_id': '<mm user id>',
             'password': '<mm user pwd>',
             'scheme': 'https',
             'port': 443,
             # Verify must be False because of our certs
             'verify': False,
}
team = 'rd'
# TODO: get this name from the lineup itself
lineup_name = 'release'

if __name__ == '__main__':

    # Attempt to login to Mattermost server
    mmd = Driver(auth_info)
    try:
        mmd.login()
    except Exception as e:
        print(f'FAILED to login: {e}')
        exit()

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--channel', dest='channel', default='Performance Lab Status', help='Channel to post message')
    parser.add_argument('-s', '--status', dest='status', choices=['updating', 'hibernating', 'down'], help='Status message to post')
    parser.add_argument('-m', '--message', dest='message', help='Additional custom message to post')
    args = parser.parse_args()

    # Try to get channel_id from channel name
    try:
        channel_id = mmd.channels.get_channel_by_name_and_team_name(team, args.channel)['id']
    except Exception as e:
        print(f'FAILED to find channel ID for {args.channel}: {e}')
        exit()

    # Set default status message
    if args.status == 'updating':
        post_message = f'{lineup_name} update is starting shortly.'
    elif args.status == 'hibernating':
        post_message = f'{lineup_name} is hibernating shortly.'
    elif args.status == 'down':
        post_message = f'{lineup_name} is currently down.'
    else:
        print(f'Unknown status option {args.status} -- how?!')
        exit()

    # Add custom status message
    if args.message:
        post_message += '\n' + args.message

    # Try to post message to channel
    try:
        mmd.posts.create_post(options={'channel_id': channel_id,
                                       'message': post_message})
    except Exception as e:
        print(f'FAILED to post message: {e}')
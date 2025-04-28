import discord
import asyncio

# Create a client instance with the appropriate intents
intents = discord.Intents.default()
intents.messages = True  # Enable the message events
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    channel_id = 00000000000000000  # Replace with your channel ID
    channel = client.get_channel(channel_id)

    if channel is not None:
        last_message_id = None
        total_messages = 0
        deleted_msgs = 0

        with open('discord_messages.txt', 'w', encoding='utf-8') as file:
            while True:
                if last_message_id is None:
                    messages = [message async for message in channel.history(limit=100)]
                else:
                    messages = [message async for message in channel.history(limit=100, before=discord.Object(id=last_message_id))]

                if not messages:
                    break

                for message in messages:
                    if not message.author.bot:  # Check if the author is not a bot
                        file.write(f'{message.author}: {message.content}\n')

                        if message.reference:
                            try:
                                ref_message = await channel.fetch_message(message.reference.message_id)
                                file.write(f'    Reply from {ref_message.author}: {ref_message.content}\n')
                            except discord.NotFound:
                                file.write('    Referenced message not found.\n')
                    else:
                        await message.delete()
                        deleted_msgs += 1
                        await asyncio.sleep(1)  # Sleep to avoid hitting rate limits

                total_messages += len(messages)
                last_message_id = messages[-1].id
                print(f'Fetched {len(messages)} messages, total so far: {total_messages}')

            print(f'Total number of messages in the channel: {total_messages}')
            print(f'Total messages deleted: {deleted_msgs}')
            print('Deleting is finished!')

    else:
        print("Channel not found!")
# Run the bot with your token
client.run('Your bot token')

# LEGACY COMMANDS
#
# def get_custom_event():
#     if sent_message.startswith("next event"):
#         event_file = stored_next_clan_event
#     if sent_message.startswith("upcoming events"):
#         event_file = stored_upcoming_clan_events
#     with open(event_file, 'r') as file:
#         clan_event = file.read()
#         clan_event = clan_event.split(clan_name.lower() + ",", 1)
#         clan_event = clan_event[1].split("Event ends here!", 1)
#     return clan_event[0]
#
# @client.event
# async def get_current_event():
#     clan_name_to_print = clan_name.replace('_', ' ')
#     try:
#         await channel.send(get_custom_event())
#     except:
#         await channel.send(clan_name_to_print + " has no custom events at this time.")
#
#
# @client.event
# async def set_event():
#     event_set = ""
#     is_searching_event = True
#
#     if sent_message.startswith("set next event:"):
#         event_file = stored_next_clan_event
#         event_set = sent_message.replace("set next event:", "")
#     if sent_message.startswith("set upcoming events:"):
#         event_file = stored_upcoming_clan_events
#         event_set = sent_message.replace("set upcoming events:", "")
#
#     with open(event_file, 'r') as file:
#         clan_event = file.read()
#
#     if clan_name + "," not in clan_event:
#         with open(event_file, 'a') as outputfile:
#             outputfile.writelines('{0},{1}{2}'.format(clan_name.lower(), event_set, "Event ends here!\n"))
#     else:
#         file = open(event_file, "r")
#         lines = file.readlines()
#         file.close()
#         file = open(event_file, "w")
#         for line in lines:
#             if not line.startswith(clan_name + ",") and is_searching_event:
#                 file.write(line)
#             else:
#                 is_searching_event = "Event ends here!" in line
#
#         file.close()
#
#         with open(event_file, 'a') as output_file:
#             output_file.writelines('{0},{1}{2}'.format(clan_name.lower(), event_set, "Event ends here!\n"))
#
#     await channel.send("These events have been set")

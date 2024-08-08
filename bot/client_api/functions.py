import asyncio
from telethon import functions
from telethon import TelegramClient
from telethon.errors import ChannelPrivateError
from telethon.types import (
    DialogFilter, Channel, InputChannel, PeerChannel, 
    ChannelParticipantsAdmins, ChannelParticipantCreator, ChatInviteExported  
)
from .password import compute_hash, compute_check


async def get_folders(client: TelegramClient) -> list[str]:
    req = await client(functions.messages.GetDialogFiltersRequest())
    return [f.title for f in req.filters if isinstance(f, DialogFilter)]


async def get_groups_from_folders(client: TelegramClient, folders: list, 
                                  only_ids=False) -> list[tuple[Channel, ChatInviteExported]]:
    req = await client(functions.messages.GetDialogFiltersRequest())
    me = await client.get_me()

    groups = []
    for f in req.filters:
        if not isinstance(f, DialogFilter) or f.title not in folders:
            continue

        for group in f.include_peers:
            if only_ids:
                groups.append(group.channel_id)
                continue

            try:
                group_data = await client.get_entity(group)
            except ChannelPrivateError:
                continue

            if isinstance(group_data, Channel):
                creator = await get_group_creator(client, group_data)
                
                if creator.user_id != me.id:
                    continue

                invite = await client(functions.messages.ExportChatInviteRequest(
                    peer=group
                ))
                groups.append((group_data, invite))
                
            await asyncio.sleep(0.3)
    return groups


async def get_group_member(client: TelegramClient, user_id, group_id: int):
    group = await client.get_entity(PeerChannel(group_id))
    
    async for user in client.iter_participants(group):
        if user.id == user_id:
            return user

    return None


async def get_password_hash(client: TelegramClient, password: str):
    request = await client(functions.account.GetPasswordRequest())
    pwd_hash = compute_hash(request.current_algo, password)

    return pwd_hash


async def transfer_group_ownership(
        client: TelegramClient, 
        password_hash: bytes, 
        user_id: int, 
        group_id: int
    ) -> ChannelParticipantCreator | None:

    group = await client.get_entity(PeerChannel(group_id))
    pwd_request = await client(functions.account.GetPasswordRequest())
    srp_pwd = compute_check(pwd_request, password_hash)
    
    await client(functions.channels.EditCreatorRequest(
        channel=group,
        user_id=user_id,
        password=srp_pwd
    ))

    new_creator = await get_group_creator(client, group)
    if user_id != new_creator.user_id:
        return None
        
    return new_creator


async def get_group_creator(client: TelegramClient, 
                            group: InputChannel) -> ChannelParticipantCreator | None:
    result = await client(functions.channels.GetParticipantsRequest(
        channel=group,
        filter=ChannelParticipantsAdmins(),
        offset=0,
        limit=100,
        hash=group.access_hash
    ))

    user = next((user for user in result.participants 
                 if isinstance(user, ChannelParticipantCreator)), None)
    if not user:
        return None

    return user


async def leave_group(client: TelegramClient, group_id: int):
    group = await client.get_entity(PeerChannel(group_id))

    await client(functions.channels.LeaveChannelRequest(
        channel=group
    ))
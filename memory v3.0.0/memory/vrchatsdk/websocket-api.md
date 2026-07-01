---
title: "Websocket API"
category: vrchatsdk
knowledge_level: applied
status: active
source: 本地知识库整理
source_type: community
version: 1.0
last_review: 2026-06-20
confidence: Medium
tags:
  - vrchatsdk
  - json
  - avatar
aliases:
  - "Websocket API"
  - 03_Websocket_API
related:
  - "tags.md"
  - "api-avatars.md"
  - "api-favorites.md"
  - "model-user.md"
  - "model-current-user.md"
---
---
source: https://vrchat.community/websocket
date: 2026-06-10
---

# Websocket API

VRChat's Websocket API, also known as "the pipeline", is used receiving updates regarding the API, such as receiving an invite request. The connection is receive-only, meaning that you can only listen for messages. Sending messages is undefined behavior.

## Connecting

Connecting to the VRChat webhook server is done via the URL:

```
wss://pipeline.vrchat.cloud/?authToken=authcookie_...
```

The `authToken` query parameter is the authorization cookie you receive when logging into VRChat. A proper User-Agent is also required to connect to the websocket server. It is possible to be connected from multiple locations at the same time. All clients will receive the exact same messages.

Most messages are double-encoded!

All notification `content` values will be documented in JSON object form. The "`content`" field is a stringified version of the JSON object, and needs to be unpacked separately.

```json
{
  "type": "notification",
  "content": "{\"userId\": \"usr_...\"}"
}
```

## Note on Enumerations

Throughout both APIs, the empty string `""` is returned in places where it would seem otherwise reasonable to have a `null` or undefined value.

### :locationString

- `"traveling"` Indicates a user's client is travelling between instances (e.g., downloading world, synchronizing world state)
- Also can be `"traveling:traveling"`

### :platformString

- `""` Pseudo-null value
- `"standalonewindows"` Desktop VRChat
- `"android"` Quest version
- `"web"` User is on a https://vrchat.com/home page
- other values Some other platform or third-party application

### :contentRefreshContentTypeEnum

- `"gallery"`, `"icon"`, `"emoji"`, `"print"`, `"prints"`, `"sticker"`, `"inventory"`, `"avatar"`, `"world"`

### :contentRefreshActionTypeEnum

- `"created"`, `"deleted"`, `"add"*`, `"delete"*`

### :inventoryType

- `"sticker"`, `"emoji"`, `"bundle"`, `"prop"`

## Events

### Notification Events

#### notification

```json
{
  "type": "notification",
  "content": {
    // Notification object
  }
}
```

#### response-notification

```json
{
  "type": "response-notification",
  "content": {
    "notificationId": ":notificationId",
    "receiverId": ":userId",
    "responseId": ":notificationId"
  }
}
```

#### see-notification

```json
{
  "type": "see-notification",
  "content": ":notificationId"
}
```

#### hide-notification

```json
{
  "type": "hide-notification",
  "content": ":notificationId"
}
```

#### clear-notification

```json
{
  "type": "clear-notification"
}
```

### NotificationV2 Events

#### notification-v2

```json
{
  "type": "notification-v2",
  "content": {
    "id": ":notificationId",
    "version": 2,
    "type": ":notificationV2TypeEnum",
    "category": ":notificationV2CategoryEnum",
    "isSystem": <boolean>,
    "ignoreDND": <boolean>,
    "senderUserId": ":userId",
    "senderUsername": ":username",
    "receiverUserId": ":userId",
    "title": ":string",
    "message": ":string",
    "imageUrl": ":assetUrl",
    "link": ":notificationLinkUri",
    "expiresAt": "dateTimeString",
    "seen": <boolean>,
    "createdAt": ":dateTimeString"
  }
}
```

#### notification-v2-update

```json
{
  "type": "notification-v2-update",
  "content": {
    "id": ":notificationId",
    "version": 2,
    "updates": {}
  }
}
```

#### notification-v2-delete

```json
{
  "type": "notification-v2-delete",
  "content": {
    "ids": [":notificationId"],
    "version": 2
  }
}
```

---

### Friend Events

#### friend-add

```json
{
  "type": "friend-add",
  "content": {
    "userId": ":userId",
    "user": { /* User object */ }
  }
}
```

#### friend-delete

```json
{
  "type": "friend-delete",
  "content": {
    "userId": ":userId"
  }
}
```

#### friend-online

```json
{
  "type": "friend-online",
  "content": {
    "userId": ":userId",
    "platform": ":platformString",
    "location": ":locationString",
    "canRequestInvite": <boolean>,
    "user": { /* User object */ }
  }
}
```

#### friend-active

```json
{
  "type": "friend-active",
  "content": {
    "userId": ":userId",
    "platform": ":platformString",
    "user": { /* User object */ }
  }
}
```

#### friend-offline

```json
{
  "type": "friend-offline",
  "content": {
    "userId": ":userId",
    "platform": ":platformString"
  }
}
```

#### friend-update

```json
{
  "type": "friend-update",
  "content": {
    "userId": ":userId",
    "user": { /* User object */ }
  }
}
```

#### friend-location

```json
{
  "type": "friend-location",
  "content": {
    "userId": ":userId",
    "location": ":locationString",
    "travelingToLocation": ":locationString",
    "worldId": ":worldId",
    "canRequestInvite": <boolean>,
    "user": { /* User object */ }
  }
}
```

---

### User Events

#### user-update

```json
{
  "type": "user-update",
  "content": {
    "userId": ":userId",
    "user": {
      "bio": ":bioString",
      "currentAvatar": ":avatarId",
      "displayName": ":displayName",
      "status": ":statusEnum",
      "statusDescription": ":statusString",
      "tags": [":tag"],
      "username": ":username"
    }
  }
}
```

#### user-location

```json
{
  "type": "user-location",
  "content": {
    "userId": ":userId",
    "user": { /* User object */ },
    "location": ":locationString",
    "instance": ":instanceId",
    "travelingToLocation": ":locationString"
  }
}
```

#### user-badge-assigned

```json
{
  "type": "user-badge-assigned",
  "content": {
    "badge": ":badge"
  }
}
```

#### user-badge-unassigned

```json
{
  "type": "user-badge-unassigned",
  "content": {
    "badgeId": ":badgeId"
  }
}
```

#### content-refresh

```json
{
  "type": "content-refresh",
  "content": {
    "contentType": ":contentRefreshContentTypeEnum",
    "fileId": ":id",
    "itemId": ":inventoryId",
    "itemType": ":inventoryType",
    "actionType": ":contentRefreshActionTypeEnum"
  }
}
```

#### economy-update

```json
{
  "type": "economy-update",
  "content": {
    "dirtyPurchases": <boolean>
  }
}
```

#### modified-image-update

```json
{
  "type": "modified-image-update",
  "content": {
    "fileId": ":id",
    "pixelSize": <number>,
    "versionNumber": <number>,
    "needsProcessing": <boolean>
  }
}
```

#### instance-queue-joined

```json
{
  "type": "instance-queue-joined",
  "content": {
    "instanceLocation": ":locationString",
    "position": <number>
  }
}
```

#### instance-queue-ready

```json
{
  "type": "instance-queue-ready",
  "content": {
    "instanceLocation": ":locationString",
    "expiry": ":dateTimeString"
  }
}
```

---

### Group Events

#### group-joined

```json
{
  "type": "group-joined",
  "content": {
    "groupId": ":groupId"
  }
}
```

#### group-left

```json
{
  "type": "group-left",
  "content": {
    "groupId": ":groupId"
  }
}
```

#### group-member-updated

```json
{
  "type": "group-member-updated",
  "content": {
    "member": { /* GroupLimitedMember object */ }
  }
}
```

#### group-role-updated

```json
{
  "type": "group-role-updated",
  "content": {
    "role": { /* GroupRole object */ }
  }
}
```
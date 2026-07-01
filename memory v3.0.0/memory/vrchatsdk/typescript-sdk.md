---
title: "VRChat.js - JavaScript SDK"
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
  - contact
  - udonsharp
aliases:
  - "VRChat.js - JavaScript SDK"
  - 02_TypeScript_SDK
related:
  - "tags.md"
  - "faq.md"
  - "api-authentication.md"
  - "api-users.md"
  - "api-worlds.md"
---
---
source: https://vrchat.community/javascript
date: 2026-06-10
---

# VRChat.js - JavaScript SDK

VRChat.js is a JavaScript SDK for interacting with the VRChat API, allowing developers to create applications that can access and manipulate VRChat data.

vrchatapi / vrchatapi-javascript65

## Install

To use the VRChat.js SDK, you need to install it using one of the following methods:

```
npm install vrchat
pnpm add vrchat
yarn add vrchat
bun add vrchat
```

## Usage

You can import the VRChat class from the SDK and create an instance of it, providing your application details such as name, version, and contact information.

```javascript
import { VRChat } from "vrchat";

const vrchat = new VRChat({
  application: {
    name: "Example",
    version: "1.5.1",
    contact: "[email protected]"
  },
});
```

### Authentication

#### Automatic (recommended)

```javascript
import { VRChat } from "vrchat";

const vrchat = new VRChat({
  authentication: {
    credentials: {
      username: "",
      password: "",
      twoFactorCode: "",
    }
  }
});

const { data: user } = await vrchat.getCurrentUser({ throwOnError: true });
console.log(`Logged in as ${data.displayName}.`);
```

#### Optimistic

By default, when given credentials, the SDK will immediately attempt to log in using the provided credentials.

```javascript
const vrchat = new VRChat({
  authentication: {
    optimistic: false,
    // ...
  }
});
```

#### On-demand (lazy authentication)

```javascript
const vrchat = new VRChat({
  application: { /* ... */ },
  authentication: {
    credentials: async () => ({
      username: "",
      password: "",
      twoFactorCode: "",
    })
  }
});
```

#### Manually (using login(...))

```javascript
const { data: user } = await vrchat
  .getCurrentUser({ throwOnError: true })
  .catch(async (error) => {
    if (!(error instanceof VRChatError) || error.statusCode !== 401)
      throw error;

    return vrchat.login({
      username,
      password,
      twoFactorCode: async () => {
        const { code } = await prompts({
          name: "code",
          type: "text",
          message: "Two-factor authentication code",
        });
        return code;
      },
      throwOnError: true,
    });
  });
```

### Persistent sessions across restarts

```javascript
import KeyvFile from "keyv-file";
import { VRChat } from "vrchat";

const vrchat = new VRChat({
  application: { /* ... */ },
  keyv: new KeyvFile({ filename: "./data.json" }),
});
```

### API Methods

```
vrchat.acceptFriendRequest
vrchat.addFavorite
vrchat.addGroupGalleryImage
vrchat.addGroupMemberRole
vrchat.addGroupPost
vrchat.addTags
vrchat.banGroupMember
vrchat.cancelGroupRequest
vrchat.cancelPending2FA
vrchat.checkUserExists
vrchat.checkUserPersistenceExists
vrchat.clearAllPlayerModerations
vrchat.clearFavoriteGroup
vrchat.clearNotifications
vrchat.closeInstance
vrchat.confirmEmail
vrchat.createAvatar
vrchat.createFile
vrchat.createFileVersion
vrchat.createGroup
vrchat.createGroupAnnouncement
vrchat.createGroupGallery
vrchat.createGroupInvite
vrchat.createGroupRole
vrchat.createInstance
vrchat.createWorld
vrchat.deleteAvatar
vrchat.deleteFile
vrchat.deleteFileVersion
vrchat.deleteFriendRequest
vrchat.deleteGroup
vrchat.deleteGroupAnnouncement
vrchat.deleteGroupGallery
vrchat.deleteGroupGalleryImage
vrchat.deleteGroupInvite
vrchat.deleteGroupPost
vrchat.deleteGroupRole
vrchat.deleteImpostor
vrchat.deleteNotification
vrchat.deletePrint
vrchat.deleteUser
vrchat.deleteUserPersistence
vrchat.deleteWorld
vrchat.disable2FA
vrchat.downloadFileVersion
vrchat.editPrint
vrchat.enable2FA
vrchat.enqueueImpostor
vrchat.finishFileDataUpload
vrchat.friend
vrchat.getActiveWorlds
vrchat.getAssignedPermissions
vrchat.getAvatar
vrchat.getBalance
vrchat.getConfig
vrchat.getCss
vrchat.getCurrentOnlineUsers
vrchat.getCurrentSubscriptions
vrchat.getCurrentUser
vrchat.getFavoritedAvatars
vrchat.getFavoritedWorlds
vrchat.getFavoriteGroup
vrchat.getFavoriteGroups
vrchat.getFavoriteLimits
vrchat.getFavorites
vrchat.getFile
vrchat.getFileAnalysis
vrchat.getFileAnalysisSecurity
vrchat.getFileAnalysisStandard
vrchat.getFileDataUploadStatus
vrchat.getFiles
vrchat.getFriends
vrchat.getFriendStatus
vrchat.getGroup
vrchat.getGroupAnnouncements
vrchat.getGroupAuditLogs
vrchat.getGroupBans
vrchat.getGroupGalleryImages
vrchat.getGroupInstances
vrchat.getGroupInvites
vrchat.getGroupMember
vrchat.getGroupMembers
vrchat.getGroupPermissions
vrchat.getGroupPosts
vrchat.getGroupRequests
vrchat.getGroupRoles
vrchat.getGroupRoleTemplates
vrchat.getImpostorQueueStats
vrchat.getInfoPush
vrchat.getInstance
vrchat.getInstanceByShortName
vrchat.getInviteMessage
vrchat.getInviteMessages
vrchat.getJam
vrchat.getJams
vrchat.getJamSubmissions
vrchat.getJavaScript
vrchat.getLicensedAvatars
vrchat.getLicenseGroup
vrchat.getNotification
vrchat.getNotifications
vrchat.getOwnAvatar
vrchat.getPermission
vrchat.getPlayerModerations
vrchat.getPrint
vrchat.getProductListing
vrchat.getProductListings
vrchat.getRecentWorlds
vrchat.getRecoveryCodes
vrchat.getShortName
vrchat.getSteamTransactions
vrchat.getSubscriptions
vrchat.getSystemTime
vrchat.getTiliaStatus
vrchat.getTiliaTos
vrchat.getTokenBundles
vrchat.getUser
vrchat.getUserGroupInstances
vrchat.getUserGroupRequests
vrchat.getUserGroups
vrchat.getUserNote
vrchat.getUserNotes
vrchat.getUserPrints
vrchat.getUserRepresentedGroup
vrchat.getWorld
vrchat.getWorldInstance
vrchat.getWorldPublishStatus
vrchat.inviteMyselfTo
vrchat.inviteUser
vrchat.inviteUserWithPhoto
vrchat.joinGroup
vrchat.kickGroupMember
vrchat.leaveGroup
vrchat.login
vrchat.logout
vrchat.markNotificationAsRead
vrchat.moderateUser
vrchat.publishWorld
vrchat.removeFavorite
vrchat.removeGroupMemberRole
vrchat.removeTags
vrchat.requestInvite
vrchat.requestInviteWithPhoto
vrchat.resendEmailConfirmation
vrchat.resetInviteMessage
vrchat.respondGroupJoinRequest
vrchat.respondInvite
vrchat.respondInviteWithPhoto
vrchat.searchAvatars
vrchat.searchGroups
vrchat.searchUsers
vrchat.searchWorlds
vrchat.selectAvatar
vrchat.selectFallbackAvatar
vrchat.setCredentials
vrchat.startFileDataUpload
vrchat.unbanGroupMember
vrchat.unfriend
vrchat.unmoderateUser
vrchat.unpublishWorld
vrchat.updateAvatar
vrchat.updateBadge
vrchat.updateFavoriteGroup
vrchat.updateGroup
vrchat.updateGroupGallery
vrchat.updateGroupMember
vrchat.updateGroupPost
vrchat.updateGroupRepresentation
vrchat.updateGroupRole
vrchat.updateInviteMessage
vrchat.updateUser
vrchat.updateUserNote
vrchat.updateWorld
vrchat.uploadGalleryImage
vrchat.uploadIcon
vrchat.uploadImage
vrchat.uploadPrint
vrchat.verify2FA
vrchat.verify2FaEmailCode
vrchat.verifyAuthToken
vrchat.verifyLoginPlace
vrchat.verifyPending2FA
vrchat.verifyRecoveryCode
```

## FAQ

### Error: You must provide an application name, version, and contact information.

```typescript
import { VRChat } from "vrchat";

const vrchat = new VRChat({
  application: {
    name: "Example",
    version: "1.5.1",
    contact: "[email protected]"
  }
});
```
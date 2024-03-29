# Transcendence API documentation

this documentation details the different endpoints of each microservice.


## Front
> ### [Router](../front/doc/router.md)
>
> ##### A client side router for single page application

> ### [Component](../front/doc/component.md)
>
> ##### A custom HTML element for building web components

> ### [Cookies](../front/doc/cookies.md)
>
> ##### A simple and convenient way to manage cookies in a web application

## Matchmaking
> ### [Events sent by the client](../matchmaking/doc/matchmaking.md#events-sent-by-the-client)

> ### [Events sent by the server](../matchmaking/doc/matchmaking.md#events-sent-by-the-server)

## Game

> ### [Game creator](../pong_server/doc/game_creator.md)
> ##### Create game servers

> ### [Game server](../pong_server/doc/game_server.md)
> ##### Play a game

## Tournament

> ### [/tournament](../tournament/doc/tournament.md#tournament)
> 
> #### Create / retrieve tournament
 
> ### [/tournament/self](../tournament/doc/tournament.md#tournamentself)
>
> #### Manage user's tournaments

> ### [/tournament/{id}](../tournament/doc/tournament.md#tournamentid)
>
> #### Manage a tournament

> ### [/tournament/{id}/players](../tournament/doc/tournament.md#tournamentidplayers)
>
> #### Manage players of a tournament

> ### [/tournament/{id}/matches](../tournament/doc/tournament.md#tournamentidmatches)
>
> #### Manage matches of a tournament

> ### [/tournament/{id}/match](../tournament/doc/tournament.md#tournamentidmatch)
>
> #### Manage matches of a tournament

## User Management
> ### [/user/signup](../user_management/doc/user_management.md#usersignup)
> ### [/user/signin](../user_management/doc/user_management.md#usersignin)
> ### [/user/verify-email/\<str:id\>/\<str:token\>](../user_management/doc/user_management.md#userverify-emailstridstrtoken)
>
> #### Create an account / Sign in

> ### [/user/username-exist](../user_management/doc/user_management.md#userusername-exist)
> ### [/user/email-exist](../user_management/doc/user_management.md#useremail-exist)
>
> #### Check if a username / email already exists

> ### [/user/forgot-password/send-code](../user_management/doc/user_management.md#userforgot-passwordsend-code)
> ### [/user/forgot-password/check-code](../user_management/doc/user_management.md#userforgot-passwordcheck-code)
> ### [/user/forgot-password/change-password](../user_management/doc/user_management.md#userforgot-passwordchange-password)
>
> #### Forgot password process

> ### [/user/update-infos/](../user_management/doc/user_management.md#userupdate-infos)
> ### [/user/avatar/](../user_management/doc/user_management.md#useravatar)
> ### [/user/delete-account/](../user_management/doc/user_management.md#userdelete-account)
>
> #### Update/delete user information

> ### [/user/id/{user_id}](../user_management/doc/user_management.md#useriduser-id)
> ### [/user/id_list/](../user_management/doc/user_management.md#userid-list)
> ### [/user/search-username/](../user_management/doc/user_management.md#usersearch-username)
> ### [/user/me/](../user_management/doc/user_management.md#userme)
>
> #### Retrieve user information

> ### [/user/refresh-access-jwt](../user_management/doc/user_management.md#userrefresh-access-jwt)
>
> #### Refresh the access token

> ### [/user/oauth/{oauth-service}](../user_management/doc/user_management.md#useroauthoauth-service)
> ### [/user/oauth/callback/{oauth-service}](../user_management/doc/user_management.md#useroauthcallbackauth-service)
>
> #### Oauth2 process

> ### [/user/2fa/enable](../user_management/doc/user_management.md#user2faenable)
> ### [/user/2fa/disable](../user_management/doc/user_management.md#user2fadisable)
> ### [/user/2fa/verify](../user_management/doc/user_management.md#user2faverify)
>
> #### Two factor authentication process

> ### [/user/friends/](../user_management/doc/user_management.md#userfriends)
> ### [/user/friends/request/](../user_management/doc/user_management.md#userfriendsrequest)
> ### [/user/friends/accept/](../user_management/doc/user_management.md#userfriendsaccept)
> ### [/user/friends/decline/](../user_management/doc/user_management.md#userfriendsdecline)
> ### [/user/friends/status/](../user_management/doc/user_management.md#userfriendsstatus)
>
> #### Manage friends

> ### [/user/send-user-infos/](../user_management/doc/user_management.md#usersend-user-infos)
> 
> #### Send user information via its email (GDPR)


## User Stats 
> ### [/statistics/user/{id}](../user_stats/doc/user_stats.md#statisticsuserid)

> ### [/statistics/user/{id}/progress/](../user_stats/doc/user_stats.md#statisticsuseridprogress)
 
> ### [/statistics/user/{id}/graph/](../user_stats/doc/user_stats.md#statisticsuseridgraph)
 
> ### [/statistics/user/{id}/history/](../user_stats/doc/user_stats.md#statisticsuseridhistory)

> ### [/statistics/user/{id}/friends/](../user_stats/doc/user_stats.md#statisticsuseridfriends)

> ### [/statistics/match/](../user_stats/doc/user_stats.md#statisticsmatch)

> ### [/statistics/ranking/](../user_stats/doc/user_stats.md#statisticsranking)

## Notification

> ### [/notification/user/](../notification/doc/notification.md#notificationuser)

> ### [/notification/user/{notification_id}/](../notification/doc/notification.md#notificationusernotification_id)

> ### [/notification/friend/add/](../notification/doc/notification.md#notificationfriendadd)

> ### [/notification/friend/delete/](../notification/doc/notification.md#notificationfrienddelete)

## Template

> ### [/template](Template_api_Documentation.md#template)
>
> #### Create / retrieve template

> ### [/template/{id}](Template-API-Documentation.md#templateid)
>
> #### Retrieve information from a specific template

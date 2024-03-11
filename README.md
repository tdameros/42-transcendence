# Transcendence

Transcendence is a project at 42 School aimed at introducing us to the web by creating a competitive multiplayer Pong.


<table align=center>
	<thead>
		<tr>
			<th colspan=2>Some renders</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td><image src="assets/homepage.png"></image></td>
			<td><image src="assets/pong.png"></image></td>
		</tr>
	</tbody>
</table>




## Usage

Generate the `.env` file using .env.example as a template.

```bash
cp .env_example .env
```

Generate .env files for each service

```bash
make generate_env
```

Start microservices

```bash
make
```

## Features

- Remote player
- Remote authentication
- Microservices architecture
- 3D pong game
- GDPR compliant
- User and game statistics
- Support for multiple devices
- Tournament with a maximum of 32 players
- Ranking system
- Elo based matchmaking


## Techonologies

- Docker (images only based on debian bookworm)
- Docker compose
- Python 3.12
- Django 4.2.7
- Bootstrap 5.3
- Vitejs (with only vanilla js)
- Postgres 14 and Redis 7.2.4


## Default Ports

- Front: 443
- Tournament: 6001
- User management: 6002
- User stats: 6003
- Matchmaking: 6004
- Notification: 6005
- Game creator: 6006
- Game server: 50200:50400

## Microservices Architecture

We have chosen to use a microservices architecture.

![](assets/architecture.png)

## Documentation

- [General](doc/documentation.md)
- [Front](front/doc/front.md)
- [Matchmaking](matchmaking/doc/matchmaking.md)
- [Game Creator](pong_server/doc/game_creator.md)
- [Game Server](pong_server/doc/game_server.md)
- [Tournament](tournament/doc/tournament.md)
- [User Management](user_management/doc/user_management.md)
- [Notification](notification/doc/notification.md)

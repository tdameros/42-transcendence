import {UserManagementClient} from './UserManagementClient.js';
import {UserStatsClient} from './UserStatsClient.js';
import {TournamentClient} from './TournamentClient.js';
import {NotificationClient} from './NotificationClient.js';
import {PongServerClient} from './PongServerClient.js';

export const userManagementClient = new UserManagementClient();
export const userStatsClient = new UserStatsClient();
export const tournamentClient = new TournamentClient();
export const notificationClient = new NotificationClient();

export const pongServerClient = new PongServerClient();

export {
  UserManagementClient,
  UserStatsClient,
  TournamentClient,
  NotificationClient,
  PongServerClient,
};

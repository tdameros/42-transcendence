import {UserManagementClient} from './UserManagementClient.js';
import {UserStatsClient} from './UserStatsClient.js';
import {TournamentClient} from './TournamentClient.js';

export const userManagementClient = new UserManagementClient();
export const userStatsClient = new UserStatsClient();
export const tournamentClient = new TournamentClient();

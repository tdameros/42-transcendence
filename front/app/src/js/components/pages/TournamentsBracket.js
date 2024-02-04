import {Component} from '../Component.js';

export class TournamentsBracket extends Component {
  constructor(matches, nbOfPlayers) {
    super();
    this.matches = matches;
    this.nbOfPlayers = nbOfPlayers;
  }
  render() {
    return (`
      <div class="container">
          <div class="tournament-bracket tournament-bracket-rounded">
              ${this.#generateBracket(this.matches, this.nbOfPlayers)}
          </div>
      </div>
    `);
  }
  style() {
    return (`
      <style>
      .tournament-bracket-list {
          padding: 0;
      }
      
      *,
      *::before,
      *::after {
          box-sizing: border-box;
      }
      
      .container {
          width: 90%;
          min-width: 18em;
          margin: 20px auto;
      }
      
      .sr-only {
          position: absolute;
          width: 1px;
          height: 1px;
          padding: 0;
          margin: -1px;
          overflow: hidden;
          clip: rect(0, 0, 0, 0);
          border: 0;
      }
      
      .tournament-bracket {
          display: flex;
          flex-direction: column;
      }
      
      @media (min-width: 38em) {
          .tournament-bracket {
              flex-direction: row;
          }
      }
      
      .tournament-bracket-round {
          display: block;
          margin-left: -3px;
          flex: 1;
      }
      
      .tournament-bracket-round-title {
          color: #9e9e9e;
          font-size: 0.95rem;
          font-weight: 400;
          text-align: center;
          font-style: italic;
          margin-bottom: 0.5em;
      }
      
      .tournament-bracket-list {
          display: flex;
          flex-direction: column;
          flex-flow: row wrap;
          justify-content: center;
          height: 100%;
          min-height: 100%;
          border-bottom: 1px dashed var(--bs-secondary-bg);
          padding-bottom: 2em;
          margin-bottom: 2em;
          transition: padding 0.2s ease-in-out, margin 0.2s ease-in-out;
      }
      
      @media (max-width: 24em) {
          .tournament-bracket-list {
              padding-bottom: 1em;
              margin-bottom: 1em;
          }
      }
      
      @media (min-width: 38em) {
          .tournament-bracket-list {
              margin-bottom: 0;
              padding-bottom: 0;
              border-right: 1px dashed var(--bs-secondary-bg);
              border-bottom: 0;
          }
      }
      
      .tournament-bracket-round:last-child .tournament-bracket-list {
          border: 0;
      }
      
      .tournament-bracket-item {
          display: flex;
          flex: 0 1 auto;
          justify-content: center;
          flex-direction: column;
          align-items: flex-start;
          position: relative;
          padding: 2% 0;
          width: 48%;
          transition: padding 0.2s linear;
      }
      
      .tournament-bracket-item:nth-child(odd) {
          margin-right: 2%;
      }
      
      .tournament-bracket-item:nth-child(even) {
          margin-left: 2%;
      }
      
      .tournament-bracket-item::after {
          transition: width 0.2s linear;
      }
      
      @media (max-width: 24em) {
          .tournament-bracket-item {
              width: 100%;
          }
      
          .tournament-bracket-item:nth-child(odd),
          .tournament-bracket-item:nth-child(even) {
              margin-left: 0;
              margin-right: 0;
          }
      }
      
      @media (min-width: 38em) {
          .tournament-bracket-item {
              padding: 0.5em 1em;
              width: 100%;
          }
      
          .tournament-bracket-item:nth-child(odd),
          .tournament-bracket-item:nth-child(even) {
              margin: 0;
          }
      
          .tournament-bracket-item::after {
              position: absolute;
              right: 0;
              content: '';
              display: block;
              width: 1em;
              height: 45%;
              border-right: 2px solid #9e9e9e;
          }
      
          .tournament-bracket-item:nth-child(odd)::after {
              top: 50%;
              border-top: 2px solid #9e9e9e;
              transform: translateY(-1px);
          }
      
          .tournament-bracket-rounded .tournament-bracket-item:nth-child(odd)::after {
              border-top-right-radius: 0.6em;
          }
      
          .tournament-bracket-item:nth-child(even)::after {
              bottom: 50%;
              border-bottom: 2px solid #9e9e9e;
              transform: translateY(1px);
          }
      
          .tournament-bracket-rounded .tournament-bracket-item:nth-child(even)::after {
              border-bottom-right-radius: 0.6em;
          }
      
          .tournament-bracket-round:first-child .tournament-bracket-item {
              padding-left: 0;
          }
      
          .tournament-bracket-round:last-child .tournament-bracket-item::after {
              display: none;
          }
      }
      
      @media (min-width: 72em) {
          .tournament-bracket-item {
              padding: 0.5em 1.5em;
          }
      
          .tournament-bracket-item::after {
              width: 1.5em;
          }
      }
      
      .tournament-bracket-match {
          display: flex;
          width: 100%;
          background-color: #ffffff;
          padding: 1em;
          border: 1px solid transparent;
          border-radius: 0.25em;
          outline: none;
          cursor: pointer;
          transition: padding 0.2s ease-in-out, border 0.2s linear;
      }
      
      .tournament-bracket-match:focus {
          border-color: var(--bs-primary);
      }
      
      .tournament-bracket-match::before,
      .tournament-bracket-match::after {
          transition: all 0.2s linear;
      }
      
      @media (max-width: 24em) {
          .tournament-bracket-match {
              padding: 0.75em 0.5em;
          }
      }
      
      @media (min-width: 38em) {
          .tournament-bracket-match::before,
          .tournament-bracket-match::after {
              position: absolute;
              left: 0;
              z-index: 1;
              content: '';
              display: block;
              width: 1em;
              height: 10%;
              border-left: 2px solid #9e9e9e;
          }
      
          .tournament-bracket-match::before {
              bottom: 50%;
              border-bottom: 2px solid #9e9e9e;
              transform: translate(0, 1px);
          }
      
          .tournament-bracket-rounded .tournament-bracket-match::before {
              border-bottom-left-radius: 0.6em;
          }
      
          .tournament-bracket-match::after {
              top: 50%;
              border-top: 2px solid #9e9e9e;
              transform: translate(0, -1px);
          }
      
          .tournament-bracket-rounded .tournament-bracket-match::after {
              border-top-left-radius: 0.6em;
          }
      }
      
      @media (min-width: 72em) {
          .tournament-bracket-match::before,
          .tournament-bracket-match::after {
              width: 1.5em;
          }
      
          .tournament-bracket-match::before {
              transform: translate(0, 1px);
          }
      
          .tournament-bracket-match::after {
              transform: translate(0, -1px);
          }
      }
      
      .tournament-bracket-round:first-child .tournament-bracket-match::before,
      .tournament-bracket-round:first-child .tournament-bracket-match::after {
          display: none;
      }
      </style>
    `);
  }

  postRender() {
    this.body = this.querySelector('.tournament-bracket');
  }

  #generateBracket(matches, nbOfPlayers) {
    const nbRound = Math.ceil(Math.log2(nbOfPlayers));
    const bracketMatches = [];
    let index = 0;
    for (let roundIndex = 0; roundIndex < nbRound; roundIndex++) {
      const currentRound = 2 ** (nbRound - roundIndex - 1);
      bracketMatches.push(matches.slice(index, index + currentRound));
      index += currentRound;
    }
    const rounds = bracketMatches.map(
        (round) => this.#generateRound(round),
    ).join('');
    return (rounds);
  }

  #generateRound(matches) {
    const matchesHtml = matches.map(
        (match) => this.#generateBracketItem(match),
    ).join('');
    return (`
          <div class="tournament-bracket-round">
              <h3 class="tournament-bracket-round-title">Top ${matches.length * 2}</h3>
              <ul class="tournament-bracket-list">
                  ${matchesHtml}
              </ul>
          </div>
      `);
  }
  #generateBracketItem(match) {
    const player1 = match['player_1'];
    const player2 = match['player_2'];
    const player1Nickname = player1 !== null ? player1['nickname'] : null;
    const player2Nickname = player2 !== null ? player2['nickname'] : null;
    if (match['player_1_score'] === null) {
      match['player_1_score'] = 0;
    }
    if (match['player_2_score'] === null) {
      match['player_2_score'] = 0;
    }
    return (`
          <li class="tournament-bracket-item">
              <div class="tournament-bracket-match bg-body-secondary p-0 justify-content-center" tabindex="0">
                  <div class="d-flex align-items-center justify-content-center" style="margin: 2px">
                      <div class="d-flex flex-column m-1">
                        ${this.#generatePlayerNickname(player1Nickname)}
                        ${this.#generatePlayerNickname(player2Nickname)}
                      </div>
                      <div class="d-flex flex-column align-items-center m-1">
                        ${this.#generatePlayerScore(player1Nickname, player2Nickname, match['player_1_score'], match['player_2_score'])}
                        ${this.#generatePlayerScore(player2Nickname, player1Nickname, match['player_2_score'], match['player_1_score'])}
                      </div>
                  </div>
              </div>
          </li>
      `);
  }

  #generatePlayerNickname(playerNickname) {
    const nicknameClass = playerNickname === null ?
      'text-muted text-opacity-25': '';
    return (`
      <div class="${nicknameClass} text-nowrap mr-2">
        ${playerNickname !== null ? playerNickname : 'Empty slot'}
      </div>
    `);
  }

  #generatePlayerScore(playerNickname, adversaryNickname,
      playerScore, adversaryScore) {
    let scoreClass;
    if (playerNickname === null) {
      scoreClass = 'text-muted text-opacity-25';
    } else if (adversaryNickname === null) {
      scoreClass = '';
    } else if (playerScore > adversaryScore) {
      scoreClass = 'text-success';
    } else if (playerScore < adversaryScore) {
      scoreClass = 'text-danger';
    } else if (playerScore === adversaryScore) {
      scoreClass = 'text-warning';
    }
    return (`
      <span class="${scoreClass} text-nowrap">
        ${playerScore !== null ? playerScore : '0'}
      </span>
    `);
  }
}

import type { BoardGame } from "../../types/api";
import "./GameList.css";

interface GameListProps {
  games: BoardGame[];
}

export function GameList({ games }: GameListProps) {
  return (
    <section className="game-list">
      <h2>My Games</h2>

      {games.length === 0 ? (
        <p className="game-list-empty">
          You don't have any games in your collection yet.
        </p>
      ) : (
        <div className="game-list-grid">
          {games.map((game) => (
            <article
              className="game-card"
              key={game.id}
            >
              {game.images.length > 0 && (
                <img
                  className="game-card-image"
                  src={game.images[0].image_url}
                  alt={game.title}
                />
              )}

              <div className="game-card-content">
                <h3>{game.title}</h3>

                <p>
                  {game.min_players}–{game.max_players} players
                </p>

                <p>
                  {game.duration_minutes} minutes
                </p>

                {game.genres.length > 0 && (
                  <div className="game-card-genres">
                    {game.genres.map((genre) => (
                      <span key={genre.id}>
                        {genre.name}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
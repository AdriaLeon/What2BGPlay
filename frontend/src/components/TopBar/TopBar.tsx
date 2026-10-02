import { FormEvent, useState } from "react";
import "./TopBar.css";

interface TopBarProps {
  isAuthenticated: boolean;
  onProfileClick: () => void;
  onSearch: (query: string) => void;
  onLoginClick: () => void;
  onRegisterClick: () => void;
  onLogout: () => void;
}

export function TopBar({
  isAuthenticated,
  onProfileClick,
  onSearch,
  onLoginClick,
  onRegisterClick,
  onLogout,
}: TopBarProps) {
  const [searchQuery, setSearchQuery] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    onSearch(searchQuery);
  }

  return (
    <header className="top-bar">
      <div className="top-bar-left">
        <button
          type="button"
          className="top-bar-button"
          onClick={onProfileClick}
          disabled={!isAuthenticated}
        >
          View Profile
        </button>
      </div>

      <form
        className="top-bar-search"
        onSubmit={handleSubmit}
      >
        <input
          type="search"
          placeholder="Search board games..."
          value={searchQuery}
          onChange={(event) => setSearchQuery(event.target.value)}
        />

        <button type="submit">
          Search
        </button>
      </form>

      <div className="top-bar-right">
        {!isAuthenticated ? (
          <>
            <button
              type="button"
              className="top-bar-button"
              onClick={onLoginClick}
            >
              Log in
            </button>

            <button
              type="button"
              className="top-bar-button primary"
              onClick={onRegisterClick}
            >
              Register
            </button>
          </>
        ) : (
          <button
            type="button"
            className="top-bar-button"
            onClick={onLogout}
          >
            Log out
          </button>
        )}
      </div>
    </header>
  );
}
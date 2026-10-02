import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { TopBar } from "../../components/TopBar/TopBar";
import { UserInfo } from "../../components/UserInfo/UserInfo";
import { GameList } from "../../components/GameList/GameList";
import { apiFetch } from "../../services/api";

import type { BoardGame, User } from "../../types/api";

import "./ProfilePage.css";

interface ProfilePageProps {
  isAuthenticated: boolean;
  onLogout: () => void;
}

export function ProfilePage({
  isAuthenticated,
  onLogout,
}: ProfilePageProps) {
  const navigate = useNavigate();

  const [user, setUser] = useState<User | null>(null);
  const [games, setGames] = useState<BoardGame[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }

    async function loadProfile() {
      try {
        setLoading(true);
        setError(null);

        const [userResponse, gamesResponse] =
          await Promise.all([
            apiFetch("/users/me"),
            apiFetch("/users/me/games"),
          ]);

        if (!userResponse.ok) {
          throw new Error("Failed to load user information");
        }

        if (!gamesResponse.ok) {
          throw new Error("Failed to load games");
        }

        const userData: User =
          await userResponse.json();

        const gamesData: BoardGame[] =
          await gamesResponse.json();

        setUser(userData);
        setGames(gamesData);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Something went wrong",
        );
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, [isAuthenticated, navigate]);

  function handleSearch(query: string) {
    if (!query.trim()) {
      return;
    }

    navigate(
      `/search?query=${encodeURIComponent(query)}`,
    );
  }

  if (loading) {
    return (
      <div className="profile-page">
        <TopBar
          isAuthenticated={isAuthenticated}
          onProfileClick={() => navigate("/profile")}
          onSearch={handleSearch}
          onLoginClick={() => navigate("/login")}
          onRegisterClick={() => navigate("/register")}
          onLogout={onLogout}
        />

        <main className="profile-content">
          <p>Loading profile...</p>
        </main>
      </div>
    );
  }

  if (error || user === null) {
    return (
      <div className="profile-page">
        <TopBar
          isAuthenticated={isAuthenticated}
          onProfileClick={() => navigate("/profile")}
          onSearch={handleSearch}
          onLoginClick={() => navigate("/login")}
          onRegisterClick={() => navigate("/register")}
          onLogout={onLogout}
        />

        <main className="profile-content">
          <p className="profile-error">
            {error ?? "Unable to load profile."}
          </p>
        </main>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <TopBar
        isAuthenticated={isAuthenticated}
        onProfileClick={() => navigate("/profile")}
        onSearch={handleSearch}
        onLoginClick={() => navigate("/login")}
        onRegisterClick={() => navigate("/register")}
        onLogout={onLogout}
      />

      <main className="profile-content">
        <UserInfo user={user} />

        <GameList games={games} />
      </main>
    </div>
  );
}
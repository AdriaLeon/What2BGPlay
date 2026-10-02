import { useNavigate } from "react-router-dom";
import { TopBar } from "../../components/TopBar/TopBar";
import "./MainPage.css";

interface MainPageProps {
  isAuthenticated: boolean;
  onLogout: () => void;
}

export function MainPage({
  isAuthenticated,
  onLogout,
}: MainPageProps) {
  const navigate = useNavigate();

  function handleSearch(query: string) {
    if (!query.trim()) {
      return;
    }

    navigate(
      `/search?query=${encodeURIComponent(query)}`
    );
  }

  return (
    <div className="main-page">
      <TopBar
        isAuthenticated={isAuthenticated}
        onProfileClick={() => navigate("/profile")}
        onSearch={handleSearch}
        onLoginClick={() => navigate("/login")}
        onRegisterClick={() => navigate("/register")}
        onLogout={onLogout}
      />

      <main className="main-content">
        <h1>Board Game Collection</h1>

        <p>
          Welcome to your board game collection.
        </p>
      </main>
    </div>
  );
}
import { FormEvent, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

import { apiFetch } from "../../services/api";

import "./AuthPage.css";

type AuthMode = "login" | "register";

interface AuthPageProps {
  onLogin: () => void;
}

export function AuthPage({ onLogin }: AuthPageProps) {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const initialMode: AuthMode =
    searchParams.get("mode") === "register"
      ? "register"
      : "login";

  const [mode, setMode] = useState<AuthMode>(initialMode);

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  function switchMode(newMode: AuthMode) {
    setMode(newMode);
    setError(null);
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError(null);
    setLoading(true);

    try {
      if (mode === "register") {
        const response = await apiFetch("/auth/register", {
          method: "POST",
          body: JSON.stringify({
            username,
            email,
            password,
          }),
        });

        if (!response.ok) {
          const data = await response.json();

          throw new Error(
            data.detail ?? "Registration failed",
          );
        }

        const formData = new URLSearchParams();

        formData.append("username", email);
        formData.append("password", password);

        const loginResponse = await apiFetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
        });

        if (!loginResponse.ok) {
        const data = await loginResponse.json();

        throw new Error(
            data.detail ?? "Login failed",
        );
        }

        const loginData = await loginResponse.json();

        localStorage.setItem(
        "access_token",
        loginData.access_token,
        );

        onLogin();
        navigate("/");

        return;
      }

        const formData = new URLSearchParams();

        formData.append("username", email);
        formData.append("password", password);

        const response = await apiFetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
        });

      if (!response.ok) {
        const data = await response.json();

        throw new Error(
          data.detail ?? "Login failed",
        );
      }

      const data = await response.json();

      localStorage.setItem(
        "access_token",
        data.access_token,
      );

      onLogin();
      navigate("/");
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

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>
          {mode === "login"
            ? "Log in"
            : "Create an account"}
        </h1>

        <div className="auth-switch">
          <button
            type="button"
            className={
              mode === "login"
                ? "auth-switch-button active"
                : "auth-switch-button"
            }
            onClick={() => switchMode("login")}
          >
            Log in
          </button>

          <button
            type="button"
            className={
              mode === "register"
                ? "auth-switch-button active"
                : "auth-switch-button"
            }
            onClick={() => switchMode("register")}
          >
            Register
          </button>
        </div>

        <form
          className="auth-form"
          onSubmit={handleSubmit}
        >
          {mode === "register" && (
            <label>
              Username

              <input
                type="text"
                value={username}
                onChange={(event) =>
                  setUsername(event.target.value)
                }
                required
              />
            </label>
          )}

          <label>
            Email

            <input
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              required
            />
          </label>

          <label>
            Password

            <input
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />
          </label>

          {error && (
            <p className="auth-error">
              {error}
            </p>
          )}

          <button
            type="submit"
            className="auth-submit"
            disabled={loading}
          >
            {loading
              ? "Please wait..."
              : mode === "login"
                ? "Log in"
                : "Register"}
          </button>
        </form>

        <button
          type="button"
          className="auth-back"
          onClick={() => navigate("/")}
        >
          Back
        </button>
      </div>
    </div>
  );
}
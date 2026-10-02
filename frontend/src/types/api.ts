export interface User {
  id: number;
  email: string;
  username: string;
}

export interface BoardGame {
  id: number;
  title: string;
  min_players: number;
  max_players: number;
  duration_minutes: number;
  description: string | null;
  genres: string[];
  images: string[];
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}
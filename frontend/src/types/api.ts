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
  genres: Genre[];
  images: GameImage[];
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface Genre {
  id: number;
  name: string;
}

export interface GameImage {
  id: number;
  image_url: string;
}
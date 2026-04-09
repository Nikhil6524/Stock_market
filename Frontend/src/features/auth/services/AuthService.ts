import { apiRequest } from "../../../lib/api";

type AuthResponse = {
  user_id: string;
  username: string;
  token: string;
};

export async function register(
  username: string,
  password: string,
): Promise<AuthResponse> {
  return apiRequest<AuthResponse>("/auth/register", {
    method: "POST",
    body: { username, password },
  });
}

export async function login(
  username: string,
  password: string,
): Promise<AuthResponse> {
  return apiRequest<AuthResponse>("/auth/login", {
    method: "POST",
    body: { username, password },
  });
}


import { API_BASE_URL } from "../app/config/env";

type RequestOptions = {
  method?: "GET" | "POST" | "DELETE";
  body?: unknown;
  token?: string | null;
};

type ApiError = {
  detail?: string | { message?: string };
};

export async function apiRequest<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const { method = "GET", body, token } = options;
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const error = (await safeJson<ApiError>(response)) ?? {};
    const detail = extractErrorMessage(error);
    throw new Error(detail || "Request failed.");
  }

  return (await safeJson<T>(response)) as T;
}

async function safeJson<T>(response: Response): Promise<T | null> {
  try {
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

function extractErrorMessage(error: ApiError): string {
  if (typeof error.detail === "string") {
    return error.detail;
  }
  if (error.detail && typeof error.detail === "object" && error.detail.message) {
    return error.detail.message;
  }
  return "Something went wrong.";
}


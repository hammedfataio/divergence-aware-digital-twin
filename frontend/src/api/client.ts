/**
 * Typed HTTP client for the DARA-DT Research API.
 *
 * This module is the frontend boundary to the FastAPI application.
 * It performs transport operations only and contains no research,
 * experimental, or runtime-assurance logic.
 */

import type {
  ExperimentSummary,
  HealthResponse,
  ProjectStatusResponse,
  ScenarioResponse,
} from "../types/api";


interface ApiErrorResponse {
  detail?: string;
}


export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}


async function request<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(path, {
    ...options,
    headers: {
      Accept: "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    let message = `DARA-DT API request failed (${response.status}).`;

    try {
      const error = (await response.json()) as ApiErrorResponse;

      if (error.detail) {
        message = error.detail;
      }
    } catch {
      // Preserve the generic error when the response is not JSON.
    }

    throw new ApiError(message, response.status);
  }

  return (await response.json()) as T;
}


export function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}


export function getProjectStatus(): Promise<ProjectStatusResponse> {
  return request<ProjectStatusResponse>("/api/project/status");
}


export function getExperiments(): Promise<string[]> {
  return request<string[]>("/api/experiments");
}


export function getExperimentResults(
  experimentId: string,
): Promise<ExperimentSummary> {
  const encodedId = encodeURIComponent(experimentId);

  return request<ExperimentSummary>(
    `/api/experiments/${encodedId}/results`,
  );
}


export function getScenarios(): Promise<string[]> {
  return request<string[]>("/api/scenarios");
}


export function runScenario(
  scenarioId: string,
): Promise<ScenarioResponse> {
  const encodedId = encodeURIComponent(scenarioId);

  return request<ScenarioResponse>(
    `/api/scenarios/${encodedId}/run`,
    {
      method: "POST",
    },
  );
}

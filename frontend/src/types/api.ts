/**
 * TypeScript contracts for the DARA-DT Research API.
 *
 * These types mirror the application-facing Pydantic schemas exposed
 * by the FastAPI backend. They contain no research or assurance logic.
 */

export type EvidenceStatus =
  | "available"
  | "stale"
  | "missing"
  | "conflicting";

export type Authority =
  | "allow"
  | "restrict"
  | "defer"
  | "fallback";

export type EvaluationOutcome =
  | "true_intervention"
  | "false_intervention"
  | "missed_intervention"
  | "correct_non_intervention";


export interface StateVariable {
  name: string;
  value: unknown;
}


export interface EntityState {
  entity_id: string;
  entity_type: string;
  variables: Record<string, unknown>;
}


export interface SystemState {
  timestamp: number | null;
  entities: EntityState[];
}


export interface DivergenceRecord {
  entity_id: string;
  variable: string;

  physical_value: unknown;
  twin_value: unknown;

  decision_relevant: boolean | null;
  decision_impacting: boolean | null;
}


export interface DecisionDependency {
  dependency: string;
  relevant: boolean;
}


export interface AIDecision {
  decision_id: string;
  action: string;

  vehicle_id: string | null;
  order_id: string | null;

  dependencies: DecisionDependency[];
}


export interface RuntimeEvidenceRecord {
  source: string;
  dependency: string;

  observed_value: unknown | null;

  timestamp: number | null;
  confidence: number | null;

  status: EvidenceStatus;
}


export interface PropagationRecord {
  origin: string;

  affected_dependency: string | null;

  source_decision: string | null;
  target_decision: string | null;

  propagating: boolean;

  path: string[];
}


export interface AssuranceResult {
  policy: string;

  authority: Authority;

  intervene: boolean;

  reason: string;

  relevant_divergence_count: number;
}


export interface GroundTruthResult {
  intervention_required: boolean;

  reason: string | null;
}


export interface EvaluationResult {
  outcome: EvaluationOutcome;

  correct: boolean;
}


export interface ScenarioResponse {
  scenario_id: string;

  description: string;

  physical_state: SystemState;

  twin_state: SystemState;

  divergences: DivergenceRecord[];

  ai_decision: AIDecision;

  runtime_evidence: RuntimeEvidenceRecord[];

  propagation: PropagationRecord[];

  assurance_results: AssuranceResult[];

  ground_truth: GroundTruthResult | null;

  evaluations: Record<string, EvaluationResult>;
}


export interface ExperimentMetric {
  policy: string;

  conditions: number;

  true_interventions: number;
  false_interventions: number;
  missed_interventions: number;
  correct_non_interventions: number;

  accuracy: number;
  precision: number;
  recall: number;

  false_intervention_rate: number;
  missed_intervention_rate: number;

  autonomy_availability: number;
}


export interface ExperimentSummary {
  experiment_id: string;

  title: string;

  status: "complete";

  conditions: number | null;

  metrics: ExperimentMetric[];

  finding: string | null;
}


export interface ProjectStatusResponse {
  project: string;

  full_name: string;

  research_domain: string;

  experimental_domain: string;

  experiments_completed: number;
  experiments_total: number;

  experimental_programme_complete: boolean;

  contribution_status: string;

  current_stage: string;
}


export interface HealthResponse {
  status: "ok";

  service: string;

  version: string;
}

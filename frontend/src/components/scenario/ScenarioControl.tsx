interface ScenarioControlProps {
  scenarios: string[];
  selectedScenario: string;
  runningScenario: boolean;
  error: string | null;
  onScenarioChange: (scenarioId: string) => void;
  onRunScenario: () => void;
}


function ScenarioControl({
  scenarios,
  selectedScenario,
  runningScenario,
  error,
  onScenarioChange,
  onRunScenario,
}: ScenarioControlProps) {
  return (
    <section className="scenario-control">
      <div className="scenario-control-header">
        <div>
          <p>EXP-010</p>
          <h2>Scenario Control</h2>
        </div>

        <span>
          {scenarios.length} frozen scenarios
        </span>
      </div>

      {scenarios.length === 0 ? (
        <p>
          No demonstration scenarios are available.
        </p>
      ) : (
        <div className="scenario-control-content">
          <div className="scenario-selector">
            <label htmlFor="scenario-select">
              Frozen EXP-010 Scenario
            </label>

            <select
              id="scenario-select"
              value={selectedScenario}
              disabled={runningScenario}
              onChange={(event) => {
                onScenarioChange(event.target.value);
              }}
            >
              {scenarios.map((scenarioId) => (
                <option
                  key={scenarioId}
                  value={scenarioId}
                >
                  {scenarioId}
                </option>
              ))}
            </select>
          </div>

          <button
            type="button"
            disabled={
              !selectedScenario ||
              runningScenario
            }
            onClick={onRunScenario}
          >
            {runningScenario
              ? "Running scenario..."
              : "Run Scenario"}
          </button>

          {error && (
            <p role="alert">
              {error}
            </p>
          )}
        </div>
      )}
    </section>
  );
}


export default ScenarioControl;

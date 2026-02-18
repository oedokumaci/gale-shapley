import { useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { PreferenceEditor } from '@/components/PreferenceEditor';
import { ResultsPanel } from '@/components/ResultsPanel';
import { AnimationPlayer } from '@/components/AnimationPlayer';
import { runMatching, runMatchingSteps } from '@/api/client';
import type { MatchingRequest, MatchingResponse, StepsResponse } from '@/types';

type ViewMode = 'edit' | 'results' | 'animation';

function App() {
  const [proposerNames, setProposerNames] = useState<string[]>([]);
  const [responderNames, setResponderNames] = useState<string[]>([]);
  const [proposerPrefs, setProposerPrefs] = useState<Record<string, string[]>>({});
  const [responderPrefs, setResponderPrefs] = useState<Record<string, string[]>>({});

  const [result, setResult] = useState<MatchingResponse | null>(null);
  const [stepsData, setStepsData] = useState<StepsResponse | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('edit');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // When a proposer is added, add them and update all responder prefs
  const addProposer = useCallback((name: string) => {
    setProposerNames((prev) => [...prev, name]);
    setProposerPrefs((prev) => ({ ...prev, [name]: [...responderNames] }));
    // Add new proposer to all responder preference lists
    setResponderPrefs((prev) => {
      const updated = { ...prev };
      for (const r of Object.keys(updated)) {
        updated[r] = [...updated[r], name];
      }
      return updated;
    });
  }, [responderNames]);

  const removeProposer = useCallback((name: string) => {
    setProposerNames((prev) => prev.filter((n) => n !== name));
    setProposerPrefs((prev) => {
      const updated = { ...prev };
      delete updated[name];
      return updated;
    });
    // Remove proposer from all responder preference lists
    setResponderPrefs((prev) => {
      const updated = { ...prev };
      for (const r of Object.keys(updated)) {
        updated[r] = updated[r].filter((p) => p !== name);
      }
      return updated;
    });
  }, []);

  const addResponder = useCallback((name: string) => {
    setResponderNames((prev) => [...prev, name]);
    setResponderPrefs((prev) => ({ ...prev, [name]: [...proposerNames] }));
    // Add new responder to all proposer preference lists
    setProposerPrefs((prev) => {
      const updated = { ...prev };
      for (const p of Object.keys(updated)) {
        updated[p] = [...updated[p], name];
      }
      return updated;
    });
  }, [proposerNames]);

  const removeResponder = useCallback((name: string) => {
    setResponderNames((prev) => prev.filter((n) => n !== name));
    setResponderPrefs((prev) => {
      const updated = { ...prev };
      delete updated[name];
      return updated;
    });
    // Remove responder from all proposer preference lists
    setProposerPrefs((prev) => {
      const updated = { ...prev };
      for (const p of Object.keys(updated)) {
        updated[p] = updated[p].filter((r) => r !== name);
      }
      return updated;
    });
  }, []);

  const reorderProposerPref = useCallback((person: string, newOrder: string[]) => {
    setProposerPrefs((prev) => ({ ...prev, [person]: newOrder }));
  }, []);

  const reorderResponderPref = useCallback((person: string, newOrder: string[]) => {
    setResponderPrefs((prev) => ({ ...prev, [person]: newOrder }));
  }, []);

  function buildRequest(): MatchingRequest {
    return {
      proposer_preferences: { ...proposerPrefs },
      responder_preferences: { ...responderPrefs },
    };
  }

  const canRun = proposerNames.length > 0 && responderNames.length > 0;

  async function handleRunMatching() {
    setLoading(true);
    setError(null);
    try {
      const res = await runMatching(buildRequest());
      setResult(res);
      setStepsData(null);
      setViewMode('results');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }

  async function handleRunAnimation() {
    setLoading(true);
    setError(null);
    try {
      const res = await runMatchingSteps(buildRequest());
      setStepsData(res);
      setResult(null);
      setViewMode('animation');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }

  function handleBackToEdit() {
    setViewMode('edit');
    setResult(null);
    setStepsData(null);
    setError(null);
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Gale-Shapley Algorithm</h1>
            <p className="text-sm text-muted-foreground">
              Interactive matching with step-by-step visualization
            </p>
          </div>
          {viewMode !== 'edit' && (
            <Button variant="outline" onClick={handleBackToEdit}>
              Back to Editor
            </Button>
          )}
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 space-y-6">
        {viewMode === 'edit' && (
          <>
            <PreferenceEditor
              proposerNames={proposerNames}
              responderNames={responderNames}
              proposerPrefs={proposerPrefs}
              responderPrefs={responderPrefs}
              onAddProposer={addProposer}
              onRemoveProposer={removeProposer}
              onAddResponder={addResponder}
              onRemoveResponder={removeResponder}
              onReorderProposerPref={reorderProposerPref}
              onReorderResponderPref={reorderResponderPref}
            />

            <Separator />

            <div className="flex gap-3 justify-center">
              <Button onClick={handleRunMatching} disabled={!canRun || loading}>
                {loading ? 'Running...' : 'Run Matching'}
              </Button>
              <Button variant="outline" onClick={handleRunAnimation} disabled={!canRun || loading}>
                {loading ? 'Running...' : 'Animate Step-by-Step'}
              </Button>
            </div>
          </>
        )}

        {error && (
          <div className="rounded-md bg-destructive/10 border border-destructive/20 p-3 text-sm text-destructive">
            {error}
          </div>
        )}

        {viewMode === 'results' && result && <ResultsPanel result={result} />}

        {viewMode === 'animation' && stepsData && (
          <AnimationPlayer
            data={stepsData}
            proposerNames={proposerNames}
            responderNames={responderNames}
          />
        )}
      </main>
    </div>
  );
}

export default App;

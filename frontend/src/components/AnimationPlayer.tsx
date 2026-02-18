import { useState, useEffect, useCallback, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { RoundVisualization } from './RoundVisualization';
import { ResultsPanel } from './ResultsPanel';
import type { StepsResponse } from '@/types';
import { Play, Pause, SkipBack, SkipForward, RotateCcw } from 'lucide-react';

interface AnimationPlayerProps {
  data: StepsResponse;
  proposerNames: string[];
  responderNames: string[];
}

export function AnimationPlayer({
  data,
  proposerNames,
  responderNames,
}: AnimationPlayerProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1000); // ms per step
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const totalSteps = data.steps.length;
  const isAtEnd = currentStep >= totalSteps;

  const stop = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    setPlaying(false);
  }, []);

  const advance = useCallback(() => {
    setCurrentStep((prev) => {
      if (prev >= totalSteps) {
        stop();
        return prev;
      }
      return prev + 1;
    });
  }, [totalSteps, stop]);

  useEffect(() => {
    if (playing) {
      intervalRef.current = setInterval(advance, speed);
      return () => {
        if (intervalRef.current) clearInterval(intervalRef.current);
      };
    }
  }, [playing, speed, advance]);

  function togglePlay() {
    if (isAtEnd) {
      setCurrentStep(0);
      setPlaying(true);
    } else {
      setPlaying(!playing);
    }
  }

  function stepBack() {
    stop();
    setCurrentStep((p) => Math.max(0, p - 1));
  }

  function stepForward() {
    stop();
    setCurrentStep((p) => Math.min(totalSteps, p + 1));
  }

  function reset() {
    stop();
    setCurrentStep(0);
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Step-by-Step Animation</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Controls */}
          <div className="flex items-center gap-2">
            <Button size="icon" variant="outline" onClick={reset} aria-label="Reset">
              <RotateCcw className="h-4 w-4" />
            </Button>
            <Button size="icon" variant="outline" onClick={stepBack} disabled={currentStep === 0} aria-label="Step back">
              <SkipBack className="h-4 w-4" />
            </Button>
            <Button size="icon" onClick={togglePlay} aria-label={playing ? 'Pause' : 'Play'}>
              {playing ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            </Button>
            <Button size="icon" variant="outline" onClick={stepForward} disabled={isAtEnd} aria-label="Step forward">
              <SkipForward className="h-4 w-4" />
            </Button>
            <span className="text-sm text-muted-foreground ml-2">
              {currentStep === 0
                ? 'Ready'
                : currentStep <= totalSteps
                  ? `Round ${currentStep} / ${totalSteps}`
                  : `Done (${totalSteps} rounds)`}
            </span>
          </div>

          {/* Speed slider */}
          <div className="flex items-center gap-3">
            <span className="text-xs text-muted-foreground w-12">Speed:</span>
            <Slider
              value={[2000 - speed]}
              onValueChange={([v]) => setSpeed(2000 - v)}
              min={0}
              max={1800}
              step={100}
              className="flex-1"
            />
            <span className="text-xs text-muted-foreground w-16">{speed}ms</span>
          </div>
        </CardContent>
      </Card>

      {/* Current round visualization */}
      {currentStep > 0 && currentStep <= totalSteps && (
        <RoundVisualization
          step={data.steps[currentStep - 1]}
          proposerNames={proposerNames}
          responderNames={responderNames}
        />
      )}

      {/* Final results */}
      {isAtEnd && <ResultsPanel result={data.final_result} />}
    </div>
  );
}

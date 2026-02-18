import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { RoundStep } from '@/types';

interface RoundVisualizationProps {
  step: RoundStep;
  proposerNames: string[];
  responderNames: string[];
}

export function RoundVisualization({
  step,
  proposerNames,
  responderNames,
}: RoundVisualizationProps) {
  const matchMap = new Map(step.tentative_matches.map((m) => [m.proposer, m.responder]));
  const reverseMatchMap = new Map(step.tentative_matches.map((m) => [m.responder, m.proposer]));
  const proposalMap = new Map(step.proposals.map((p) => [p.proposer, p.responder]));
  const rejectedSet = new Set(step.rejections.map((r) => r.proposer));
  const selfMatchSet = new Set(step.self_matches);

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm">Round {step.round}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-[1fr_auto_1fr] gap-4">
          {/* Proposers column */}
          <div className="space-y-2">
            <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
              Proposers
            </h4>
            {proposerNames.map((name) => {
              const proposed = proposalMap.get(name);
              const matched = matchMap.get(name);
              const rejected = rejectedSet.has(name);
              const selfMatched = selfMatchSet.has(name);

              let borderColor = 'border-border';
              let bg = 'bg-card';
              if (selfMatched) {
                borderColor = 'border-muted-foreground';
                bg = 'bg-muted opacity-60';
              } else if (matched) {
                borderColor = 'border-green-500';
                bg = 'bg-green-500/10';
              } else if (rejected) {
                borderColor = 'border-red-500';
                bg = 'bg-red-500/10';
              }

              return (
                <div
                  key={name}
                  className={`rounded-md border ${borderColor} ${bg} px-3 py-2 text-sm`}
                >
                  <span className="font-medium">{name}</span>
                  {proposed && (
                    <span className="text-xs text-muted-foreground ml-2">
                      &rarr; {proposed}
                    </span>
                  )}
                  {selfMatched && (
                    <span className="text-xs text-muted-foreground ml-2">(self)</span>
                  )}
                </div>
              );
            })}
          </div>

          {/* Arrow column */}
          <div className="flex flex-col items-center justify-center space-y-2 min-w-[60px]">
            {step.proposals.map((p, i) => {
              const rejected = rejectedSet.has(p.proposer);
              return (
                <div
                  key={i}
                  className={`text-xs font-mono ${
                    rejected ? 'text-red-500' : 'text-green-500'
                  }`}
                >
                  {rejected ? '---X' : '---→'}
                </div>
              );
            })}
          </div>

          {/* Responders column */}
          <div className="space-y-2">
            <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
              Responders
            </h4>
            {responderNames.map((name) => {
              const matchedWith = reverseMatchMap.get(name);
              const bg = matchedWith ? 'bg-green-500/10 border-green-500' : 'bg-card border-border';

              return (
                <div
                  key={name}
                  className={`rounded-md border ${bg} px-3 py-2 text-sm`}
                >
                  <span className="font-medium">{name}</span>
                  {matchedWith && (
                    <span className="text-xs text-muted-foreground ml-2">
                      &larr; {matchedWith}
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Summary */}
        <div className="mt-3 flex gap-4 text-xs text-muted-foreground">
          <span>
            <span className="inline-block w-2 h-2 rounded-full bg-green-500 mr-1" />
            {step.tentative_matches.length} matched
          </span>
          <span>
            <span className="inline-block w-2 h-2 rounded-full bg-red-500 mr-1" />
            {step.rejections.length} rejected
          </span>
          {step.self_matches.length > 0 && (
            <span>
              <span className="inline-block w-2 h-2 rounded-full bg-muted-foreground mr-1" />
              {step.self_matches.length} self-matched
            </span>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

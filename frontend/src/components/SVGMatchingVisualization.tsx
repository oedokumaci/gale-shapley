import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { PersonNode } from './svg/PersonNode';
import { AnimatedArrow } from './svg/AnimatedArrow';
import type { RoundStep, AnimationPhase, PersonImages } from '@/types';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface SVGMatchingVisualizationProps {
  step: RoundStep | null; // null = initial "ready" frame
  phase: AnimationPhase | null; // null = ready
  proposerNames: string[];
  responderNames: string[];
  personImages: PersonImages;
  onStepBack: () => void;
  onStepForward: () => void;
  canStepBack: boolean;
  canStepForward: boolean;
  isFinalRound: boolean;
}

const VIEW_WIDTH = 900;
const PROPOSER_X = 170;
const RESPONDER_X = 730;
const PADDING_Y = 65;
const MIN_RADIUS = 18;
const MAX_RADIUS = 28;

function computeLayout(names: string[], viewHeight: number) {
  const count = names.length;
  if (count === 0) return { positions: [] as { name: string; y: number }[], radius: MAX_RADIUS };
  const usableHeight = viewHeight - PADDING_Y * 2;
  const spacing = count > 1 ? usableHeight / (count - 1) : 0;
  const radius = Math.max(MIN_RADIUS, Math.min(MAX_RADIUS, spacing * 0.42));
  const positions = names.map((name, i) => ({
    name,
    y: count === 1 ? viewHeight / 2 : PADDING_Y + i * spacing,
  }));
  return { positions, radius };
}

function computeViewHeight(maxCount: number) {
  return Math.max(300, PADDING_Y * 2 + (maxCount - 1) * 72);
}

function arrowEndpoints(
  x1: number, y1: number, x2: number, y2: number,
  r1: number, r2: number,
) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const dist = Math.sqrt(dx * dx + dy * dy);
  if (dist === 0) return { ax1: x1, ay1: y1, ax2: x2, ay2: y2 };
  const ux = dx / dist;
  const uy = dy / dist;
  return {
    ax1: x1 + ux * (r1 + 3),
    ay1: y1 + uy * (r1 + 3),
    ax2: x2 - ux * (r2 + 3),
    ay2: y2 - uy * (r2 + 3),
  };
}

function firstName(fullName: string): string {
  // Keep compound names like "Bad Bunny" intact, otherwise use first name
  if (fullName === 'Bad Bunny') return 'Bad Bunny';
  return fullName.split(' ')[0];
}

interface NarrativeLine {
  text: string;
  color: 'neutral' | 'green' | 'red';
}

function buildProposalNarrative(step: RoundStep): NarrativeLine[] {
  return step.proposals.map((p) => ({
    text: `${firstName(p.proposer)} proposes to ${firstName(p.responder)}`,
    color: 'neutral' as const,
  }));
}

function buildResponseNarrative(step: RoundStep): NarrativeLine[] {
  const rejectedProposers = new Set(step.rejections.map((r) => r.proposer));
  const matchByResponder = new Map(step.tentative_matches.map((m) => [m.responder, m.proposer]));

  const lines: NarrativeLine[] = [];

  for (const p of step.proposals) {
    if (rejectedProposers.has(p.proposer)) {
      const preferredMatch = matchByResponder.get(p.responder);
      if (preferredMatch) {
        lines.push({
          text: `${firstName(p.responder)} rejects ${firstName(p.proposer)}, prefers ${firstName(preferredMatch)}`,
          color: 'red',
        });
      } else {
        lines.push({
          text: `${firstName(p.responder)} rejects ${firstName(p.proposer)}`,
          color: 'red',
        });
      }
    } else {
      lines.push({
        text: `${firstName(p.responder)} accepts ${firstName(p.proposer)}`,
        color: 'green',
      });
    }
  }

  return lines;
}

function buildMatchNarrative(step: RoundStep): NarrativeLine[] {
  const lines: NarrativeLine[] = [];
  for (const m of step.tentative_matches) {
    lines.push({
      text: `${firstName(m.proposer)} ↔ ${firstName(m.responder)}`,
      color: 'green',
    });
  }
  for (const name of step.self_matches) {
    lines.push({
      text: `${firstName(name)} is unmatched`,
      color: 'neutral',
    });
  }
  return lines;
}

const NARRATIVE_COLORS = {
  neutral: 'text-muted-foreground',
  green: 'text-green-600 dark:text-green-400',
  red: 'text-red-600 dark:text-red-400',
} as const;

function NarrativePanel({ lines, align }: { lines: NarrativeLine[]; align: 'left' | 'right' }) {
  if (lines.length === 0) return null;
  return (
    <div className={`flex flex-col gap-1.5 ${align === 'right' ? 'text-right' : 'text-left'}`}>
      {lines.map((line, i) => (
        <p
          key={i}
          className={`text-[11px] leading-tight ${NARRATIVE_COLORS[line.color]}`}
          style={{
            fontFamily: "'DM Sans', system-ui, sans-serif",
            animationName: 'fadeSlideIn',
            animationDuration: '0.3s',
            animationTimingFunction: 'ease-out',
            animationFillMode: 'both',
            animationDelay: `${i * 60}ms`,
          }}
        >
          {line.text}
        </p>
      ))}
    </div>
  );
}

export function SVGMatchingVisualization({
  step,
  phase,
  proposerNames,
  responderNames,
  personImages,
  onStepBack,
  onStepForward,
  canStepBack,
  canStepForward,
  isFinalRound,
}: SVGMatchingVisualizationProps) {
  const maxCount = Math.max(proposerNames.length, responderNames.length, 1);
  const viewHeight = computeViewHeight(maxCount);
  const proposerLayout = computeLayout(proposerNames, viewHeight);
  const responderLayout = computeLayout(responderNames, viewHeight);

  const isReady = step === null || phase === null;

  const proposerYMap = new Map(proposerLayout.positions.map((p) => [p.name, p.y]));
  const responderYMap = new Map(responderLayout.positions.map((p) => [p.name, p.y]));

  const matchMap = step ? new Map(step.tentative_matches.map((m) => [m.proposer, m.responder])) : new Map();
  const reverseMatchMap = step ? new Map(step.tentative_matches.map((m) => [m.responder, m.proposer])) : new Map();
  const rejectedSet = step ? new Set(step.rejections.map((r) => r.proposer)) : new Set<string>();
  const selfMatchSet = step ? new Set(step.self_matches) : new Set<string>();

  function getProposerStatus(name: string): 'default' | 'matched' | 'rejected' | 'self-matched' | 'unmatched' {
    if (isReady || phase === 'proposals') return 'default';
    if (selfMatchSet.has(name)) return 'self-matched';
    if (matchMap.has(name)) return phase === 'responses' ? 'default' : 'matched';
    if (rejectedSet.has(name)) return phase === 'responses' ? 'rejected' : 'unmatched';
    return 'default';
  }

  function getResponderStatus(name: string): 'default' | 'matched' | 'unmatched' {
    if (isReady || phase === 'proposals') return 'default';
    if (reverseMatchMap.has(name)) return phase === 'responses' ? 'default' : 'matched';
    return phase === 'matches' ? 'unmatched' : 'default';
  }

  type ArrowData = {
    key: string;
    proposer: string;
    responder: string;
    color: 'neutral' | 'green' | 'red';
  };

  const arrows: ArrowData[] = [];

  if (!isReady && step) {
    if (phase === 'proposals') {
      for (const p of step.proposals) {
        arrows.push({ key: `${p.proposer}-${p.responder}`, proposer: p.proposer, responder: p.responder, color: 'neutral' });
      }
    } else if (phase === 'responses') {
      for (const p of step.proposals) {
        const wasRejected = rejectedSet.has(p.proposer);
        arrows.push({
          key: `${p.proposer}-${p.responder}`,
          proposer: p.proposer,
          responder: p.responder,
          color: wasRejected ? 'red' : 'green',
        });
      }
    } else {
      for (const m of step.tentative_matches) {
        arrows.push({ key: `${m.proposer}-${m.responder}`, proposer: m.proposer, responder: m.responder, color: 'green' });
      }
    }
  }

  const phaseLabel = isReady
    ? null
    : phase === 'proposals' ? 'Proposals' : phase === 'responses' ? 'Responses' : 'Current Matches';

  // Compute stats: matched vs unmatched per group
  const matchedProposers = step ? step.tentative_matches.length : 0;
  const matchedResponders = step ? new Set(step.tentative_matches.map((m) => m.responder)).size : 0;
  const unmatchedProposers = proposerNames.length - matchedProposers - (step?.self_matches.length ?? 0);
  const unmatchedResponders = responderNames.length - matchedResponders;

  // Build narrative lines
  let leftNarrative: NarrativeLine[] = [];
  let rightNarrative: NarrativeLine[] = [];

  if (!isReady && step) {
    if (phase === 'proposals') {
      leftNarrative = buildProposalNarrative(step);
    } else if (phase === 'responses') {
      leftNarrative = buildProposalNarrative(step);
      rightNarrative = buildResponseNarrative(step);
    } else {
      leftNarrative = buildMatchNarrative(step);
    }
  }

  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-center">
          {/* Left: round or ready label — fixed width so center doesn't shift */}
          <div className="w-24 shrink-0">
            <CardTitle className="text-sm font-semibold" style={{ fontFamily: "'DM Sans', system-ui, sans-serif" }}>
              {isReady ? 'Ready' : `Round ${step!.round}`}
            </CardTitle>
          </div>

          {/* Center: phase nav — always centered */}
          <div className="flex-1 flex items-center justify-center gap-2">
            {isReady ? (
              <span className="text-xs text-muted-foreground">Press play to begin</span>
            ) : (
              <>
                <Button size="icon" variant="ghost" className="h-7 w-7" onClick={onStepBack} disabled={!canStepBack} aria-label="Previous phase (h)">
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <Badge variant="outline" className="text-xs font-medium px-3 min-w-[120px] justify-center">
                  {phaseLabel}
                </Badge>
                <Button size="icon" variant="ghost" className="h-7 w-7" onClick={onStepForward} disabled={!canStepForward} aria-label="Next phase (l)">
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </>
            )}
          </div>

          {/* Right: matched/unmatched stats — fixed width to balance layout */}
          <div className="w-24 shrink-0 flex justify-end">
            {!isReady && phase === 'matches' && (
              <div className="flex gap-3 text-[11px] text-muted-foreground">
                <span className="inline-flex items-center gap-1">
                  <span className="text-[10px] font-medium opacity-50">P</span>
                  <span className="inline-block w-2 h-2 rounded-full bg-green-500" />
                  {matchedProposers}
                  <span className="inline-block w-2 h-2 rounded-full bg-blue-500 ml-1" />
                  {unmatchedProposers}
                </span>
                <span className="inline-flex items-center gap-1">
                  <span className="text-[10px] font-medium opacity-50">R</span>
                  <span className="inline-block w-2 h-2 rounded-full bg-green-500" />
                  {matchedResponders}
                  <span className="inline-block w-2 h-2 rounded-full bg-blue-500 ml-1" />
                  {unmatchedResponders}
                </span>
              </div>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex gap-3 items-start">
          {/* Left narrative panel */}
          <div className="w-44 shrink-0 pt-16">
            <NarrativePanel lines={leftNarrative} align="left" />
          </div>

          {/* SVG visualization */}
          <div className="flex-1 min-w-0">
            <svg
              viewBox={`0 0 ${VIEW_WIDTH} ${viewHeight}`}
              preserveAspectRatio="xMidYMid meet"
              className="w-full h-auto"
            >
              {/* Column labels */}
              <text x={PROPOSER_X} y={28} textAnchor="middle"
                fontSize={10} fontWeight={600} letterSpacing="0.08em"
                className="fill-muted-foreground"
                style={{ fontFamily: "'DM Sans', system-ui, sans-serif" }}
              >
                PROPOSERS
              </text>
              <text x={RESPONDER_X} y={28} textAnchor="middle"
                fontSize={10} fontWeight={600} letterSpacing="0.08em"
                className="fill-muted-foreground"
                style={{ fontFamily: "'DM Sans', system-ui, sans-serif" }}
              >
                RESPONDERS
              </text>

              {/* Vertical guide lines */}
              <line x1={PROPOSER_X} y1={PADDING_Y - 15} x2={PROPOSER_X} y2={viewHeight - PADDING_Y + 15}
                className="stroke-border" strokeWidth="1" strokeDasharray="3,6" opacity={0.5} />
              <line x1={RESPONDER_X} y1={PADDING_Y - 15} x2={RESPONDER_X} y2={viewHeight - PADDING_Y + 15}
                className="stroke-border" strokeWidth="1" strokeDasharray="3,6" opacity={0.5} />

              {/* Arrows */}
              {arrows.map((a, i) => {
                const py = proposerYMap.get(a.proposer);
                const ry = responderYMap.get(a.responder);
                if (py === undefined || ry === undefined) return null;
                const { ax1, ay1, ax2, ay2 } = arrowEndpoints(
                  PROPOSER_X, py, RESPONDER_X, ry,
                  proposerLayout.radius, responderLayout.radius,
                );
                return (
                  <AnimatedArrow
                    key={a.key}
                    x1={ax1} y1={ay1} x2={ax2} y2={ay2}
                    color={a.color} visible={true} index={i}
                    dashed={phase === 'matches' && !isFinalRound}
                  />
                );
              })}

              {/* Proposer nodes */}
              {proposerLayout.positions.map((p, i) => (
                <PersonNode
                  key={p.name} name={p.name} cx={PROPOSER_X} cy={p.y}
                  radius={proposerLayout.radius} imageUrl={personImages[p.name]}
                  status={getProposerStatus(p.name)} side="left" index={i}
                />
              ))}

              {/* Responder nodes */}
              {responderLayout.positions.map((p, i) => (
                <PersonNode
                  key={p.name} name={p.name} cx={RESPONDER_X} cy={p.y}
                  radius={responderLayout.radius} imageUrl={personImages[p.name]}
                  status={getResponderStatus(p.name)} side="right" index={i}
                />
              ))}
            </svg>
          </div>

          {/* Right narrative panel */}
          <div className="w-44 shrink-0 pt-16">
            <NarrativePanel lines={rightNarrative} align="right" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

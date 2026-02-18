import { Badge } from '@/components/ui/badge';
import type { MatchingResponse } from '@/types';

interface StabilityBadgeProps {
  result: MatchingResponse;
}

export function StabilityBadge({ result }: StabilityBadgeProps) {
  if (result.is_stable) {
    return (
      <Badge className="bg-green-600 hover:bg-green-700 text-white">
        Stable Matching
      </Badge>
    );
  }

  return (
    <div className="space-y-1">
      <Badge variant="destructive">Unstable Matching</Badge>
      {result.blocking_pairs.length > 0 && (
        <div className="text-xs text-muted-foreground">
          <span className="font-medium">Blocking pairs: </span>
          {result.blocking_pairs.map(([p, r], i) => (
            <span key={i}>
              ({p}, {r}){i < result.blocking_pairs.length - 1 ? ', ' : ''}
            </span>
          ))}
        </div>
      )}
      {!result.is_individually_rational && (
        <p className="text-xs text-destructive">Not individually rational</p>
      )}
    </div>
  );
}

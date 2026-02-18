import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Separator } from '@/components/ui/separator';
import { StabilityBadge } from './StabilityBadge';
import type { MatchingResponse } from '@/types';

interface ResultsPanelProps {
  result: MatchingResponse;
}

export function ResultsPanel({ result }: ResultsPanelProps) {
  const matchEntries = Object.entries(result.matches);

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Results</CardTitle>
          <StabilityBadge result={result} />
        </div>
        <p className="text-sm text-muted-foreground">
          Completed in {result.rounds} round{result.rounds !== 1 ? 's' : ''}
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        {matchEntries.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold mb-2">Matched Pairs</h4>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Proposer</TableHead>
                  <TableHead>Responder</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {matchEntries.map(([proposer, responder]) => (
                  <TableRow key={proposer}>
                    <TableCell className="font-medium">{proposer}</TableCell>
                    <TableCell>{responder}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}

        {result.self_matches.length > 0 && (
          <>
            <Separator />
            <div>
              <h4 className="text-sm font-semibold mb-1">Self-Matched</h4>
              <p className="text-sm text-muted-foreground">
                {result.self_matches.join(', ')}
              </p>
            </div>
          </>
        )}

        {result.unmatched.length > 0 && (
          <>
            <Separator />
            <div>
              <h4 className="text-sm font-semibold mb-1">Unmatched</h4>
              <p className="text-sm text-muted-foreground">
                {result.unmatched.join(', ')}
              </p>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}

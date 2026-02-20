import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import { HelpCircle } from 'lucide-react';

export function HowItWorksDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm" className="text-muted-foreground">
          <HelpCircle className="h-3.5 w-3.5 mr-1" />
          How does it work?
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-2xl p-0 gap-0">
        <DialogHeader className="px-6 pt-6 pb-0">
          <DialogTitle
            className="text-xl font-bold tracking-tight"
            style={{ fontFamily: "'DM Sans', system-ui, sans-serif" }}
          >
            The Gale–Shapley Algorithm
          </DialogTitle>
        </DialogHeader>
        <ScrollArea className="max-h-[70vh] px-6 pb-6 pt-4">
          <div
            className="space-y-4 text-sm leading-relaxed text-foreground/90"
            style={{ fontFamily: "'DM Sans', system-ui, sans-serif" }}
          >
            <p>
              In 1962, David Gale and Lloyd Shapley proved that a simple
              procedure always produces a stable matching in a two-sided market.
              Each participant on one side ranks everyone on the other side. The
              algorithm runs in rounds. Every unmatched proposer applies to the
              highest-ranked person they have not yet approached. Each responder
              tentatively keeps the most preferred proposal received so far and
              rejects the rest. Rejected proposers move to their next choice.
              When no further proposals are made, the tentative matches become
              final.
            </p>

            <p>
              The result is stable: there is no blocking pair, meaning no two
              participants who would both prefer each other over their assigned
              partners. If the two sides differ in size, or if some matches are
              unacceptable, some participants may remain unmatched. Stability
              still holds in the formal sense, because no mutually preferred
              feasible deviation exists.
            </p>

            <p>
              The procedure has a built-in asymmetry. When one side proposes, the
              outcome is optimal for that side among all stable matchings and
              least favorable for the responding side among stable matchings.
              Switching who proposes produces a different stable allocation. The
              algorithm does not determine which side benefits. That choice is
              part of the mechanism design.
            </p>

            <p>
              In 2012, Lloyd Shapley and Alvin Roth received the Nobel Memorial
              Prize in Economic Sciences for the theory of stable allocations and
              the practice of market design. Shapley developed the theoretical
              foundations. Roth extended them to real institutions.
            </p>

            <p>
              A centralized system for assigning U.S. medical graduates to
              residencies emerged in the early 1950s and was formalized as the
              National Resident Matching Program. Decades later, Roth and
              collaborators analyzed it through the lens of deferred acceptance
              and helped redesign it in the late 1990s to better handle modern
              constraints, including couples applying jointly. The updated
              mechanism aligned the program more closely with the
              applicant-proposing version of deferred acceptance.
            </p>

            <p>
              Kidney exchange required a different technical extension.
              Incompatible donor–patient pairs form a directed compatibility
              graph. Clearinghouses search for disjoint cycles and chains that
              satisfy medical and logistical constraints, often optimizing for the
              number of transplants. Although the structure differs from
              one-to-one matching, the underlying discipline is the same: explicit
              preferences, clear rules, and a centralized algorithm that prevents
              mutually beneficial side deals. These exchanges have enabled
              thousands of additional transplants.
            </p>

            <p>
              Similar ideas reshaped public school assignment in cities such as
              New York and Boston. Families submit ranked lists of schools.
              Schools apply priority rules based on criteria such as siblings or
              location. The redesigned systems reduced strategic gaming and
              sharply lowered the number of students assigned to schools they had
              not listed under the prior process.
            </p>

            <p>
              What began as an abstract proof about stable allocations became a
              framework for allocating scarce resources in labor markets,
              education systems, and organ exchange. The core logic remains
              unchanged: collect preferences, apply a well-specified procedure,
              and produce an allocation that no pair can jointly improve upon
              outside the mechanism.
            </p>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}

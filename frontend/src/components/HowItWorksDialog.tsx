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
            The Gale-Shapley Algorithm
          </DialogTitle>
        </DialogHeader>
        <ScrollArea className="max-h-[70vh] px-6 pb-6 pt-4">
          <div
            className="space-y-4 text-sm leading-relaxed text-foreground/90"
            style={{ fontFamily: "'DM Sans', system-ui, sans-serif" }}
          >
            <p>
              Imagine a group of people on one side of a room, each holding a
              private list of who they&rsquo;d most like to be paired with on the
              other side. Everyone has ranked everyone else, and now a matchmaker
              has to pair them up so that nobody wants to run off with someone
              else&rsquo;s partner. That&rsquo;s the stable matching problem, and in 1962,
              two mathematicians &mdash; David Gale and Lloyd Shapley &mdash; proved
              something remarkable: a simple, elegant procedure always finds such
              a matching.
            </p>

            <p>
              The algorithm works in rounds. In each round, every unmatched
              proposer goes to the highest-ranked person on their list they
              haven&rsquo;t yet asked, and proposes. Each responder looks at all the
              proposals they received &mdash; including any tentative partner they&rsquo;re
              already holding &mdash; keeps the one they like best, and lets the rest
              go. Rejected proposers cross that name off their list and try again
              next round. That&rsquo;s it. The process repeats until no one is left
              proposing, and the tentative matches become final.
            </p>

            <p>
              What makes this beautiful is the guarantee. The result is always{' '}
              <em>stable</em>, meaning there is no pair of people who would both
              rather be with each other than with their assigned partner. In other
              words, no one can point across the room and say &ldquo;we&rsquo;d both be
              happier together&rdquo; &mdash; every such temptation is one-sided. This
              holds regardless of how people rank each other, regardless of the
              number of participants, every single time.
            </p>

            <p>
              There&rsquo;s an asymmetry built in: the proposing side gets the best
              stable partner they could hope for, while the responding side gets
              their worst stable partner. Swap which side proposes, and you get a
              different stable matching that favors the other group. Both are
              equally valid. The algorithm doesn&rsquo;t decide who deserves the
              advantage &mdash; only which stable outcome emerges.
            </p>

            <p className="border-l-2 border-primary/30 pl-4 text-foreground/70 italic">
              In 2012, the Nobel Memorial Prize in Economics was awarded to Lloyd
              Shapley and Alvin Roth &ldquo;for the theory of stable allocations and
              the practice of market design.&rdquo; Shapley for the theory behind this
              very algorithm, and Roth for spending decades showing the world what
              it could do.
            </p>

            <p>
              Roth discovered that the National Resident Matching Program, which
              assigns medical school graduates to hospital residencies across the
              United States, had independently reinvented something essentially
              identical to Gale-Shapley in the 1950s &mdash; before the paper was
              even published. He then helped redesign it when the original system
              started breaking down under modern pressures like couples applying
              together.
            </p>

            <p>
              But his most celebrated work came in kidney exchange. When a patient
              needs a kidney and a loved one volunteers to donate but isn&rsquo;t a
              biological match, Roth helped design exchange systems where
              incompatible pairs could be matched in cycles &mdash; your donor gives
              to my patient, my donor gives to yours &mdash; using the same
              principles of stability. Thousands of people have received
              transplants through these programs who otherwise would have waited
              years on the deceased-donor list, or never received one at all.
            </p>

            <p>
              The same ideas now run school choice systems in New York, Boston,
              and cities around the world, where families rank schools and schools
              rank applicants, and an algorithm finds an assignment where no
              student and school would both prefer each other over their current
              match. Before these systems, the assignment process in New York City
              was so broken that roughly 30,000 students a year ended up at
              schools they hadn&rsquo;t even listed.
            </p>

            <p>
              What started as a short, elegant proof about an abstract matching
              problem became one of the most practically consequential ideas in
              modern economics. The core insight is disarmingly simple: let people
              express their preferences honestly, run a transparent process, and
              the result is something no pair can improve upon by going around the
              system. It&rsquo;s a rare case where mathematical beauty and real-world
              usefulness turned out to be the same thing.
            </p>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}

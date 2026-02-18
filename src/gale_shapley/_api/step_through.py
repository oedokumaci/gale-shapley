"""Step-through execution of the Gale-Shapley algorithm, capturing per-round state."""

from gale_shapley._api.models import (
    MatchingResponse,
    ProposalAction,
    RoundStep,
    StepsResponse,
)
from gale_shapley.algorithm import Algorithm
from gale_shapley.person import Proposer, Responder
from gale_shapley.result import MatchingResult, StabilityResult
from gale_shapley.stability import check_stability


def _build_participants(
    proposer_preferences: dict[str, list[str]],
    responder_preferences: dict[str, list[str]],
) -> Algorithm:
    """Build Proposer/Responder objects and return an Algorithm instance.

    This mirrors the logic in create_matching() but returns the Algorithm
    before execution so we can step through it.
    """
    proposers = {name: Proposer(name, "proposer") for name in proposer_preferences}
    responders = {name: Responder(name, "responder") for name in responder_preferences}

    for name, pref_names in proposer_preferences.items():
        p = proposers[name]
        prefs: list[Proposer | Responder] = [responders[r] for r in pref_names if r in responders]
        if p not in prefs:
            prefs.append(p)
        for r in responders.values():
            if r not in prefs:
                prefs.append(r)
        p.preferences = tuple(prefs)

    for name, pref_names in responder_preferences.items():
        r = responders[name]
        prefs_r: list[Proposer | Responder] = [proposers[p] for p in pref_names if p in proposers]
        if r not in prefs_r:
            prefs_r.append(r)
        for p in proposers.values():
            if p not in prefs_r:
                prefs_r.append(p)
        r.preferences = tuple(prefs_r)

    return Algorithm(list(proposers.values()), list(responders.values()))


def _build_matching_response(result: MatchingResult, stability: StabilityResult) -> MatchingResponse:
    """Combine MatchingResult and StabilityResult into a MatchingResponse."""
    return MatchingResponse(
        rounds=result.rounds,
        matches=result.matches,
        unmatched=result.unmatched,
        self_matches=result.self_matches,
        all_matched=result.all_matched,
        is_stable=stability.is_stable,
        is_individually_rational=stability.is_individually_rational,
        blocking_pairs=stability.blocking_pairs,
    )


def run_step_through(  # noqa: PLR0912
    proposer_preferences: dict[str, list[str]],
    responder_preferences: dict[str, list[str]],
) -> StepsResponse:
    """Run the algorithm step by step, capturing a RoundStep per round."""
    algorithm = _build_participants(proposer_preferences, responder_preferences)
    steps: list[RoundStep] = []

    while not algorithm.terminate():
        round_num = algorithm.round + 1

        # Capture who is unmatched before proposing
        unmatched_before = {p.name for p in algorithm.unmatched_proposers}

        # Proposers propose
        algorithm.proposers_propose()

        # After proposing, capture proposals by inspecting last_proposal
        proposals: list[ProposalAction] = []
        round_self_matches: list[str] = []
        for proposer in algorithm.proposers:
            if proposer.name not in unmatched_before:
                continue
            # If proposer proposed to themselves, it's a self-match
            if proposer.last_proposal is proposer:
                round_self_matches.append(proposer.name)
            elif proposer.last_proposal is not None and isinstance(proposer.last_proposal, Responder):
                proposals.append(ProposalAction(proposer=proposer.name, responder=proposer.last_proposal.name))

        # Responders respond
        algorithm.responders_respond()
        algorithm.round += 1

        # After responding, determine rejections and tentative matches
        rejections: list[ProposalAction] = []
        tentative_matches: list[ProposalAction] = []

        for proposer in algorithm.proposers:
            if proposer.name not in unmatched_before:
                # Already matched from a previous round - still tentatively matched
                if (
                    proposer.match is not None
                    and proposer.match is not proposer
                    and isinstance(proposer.match, Responder)
                ):
                    tentative_matches.append(ProposalAction(proposer=proposer.name, responder=proposer.match.name))
                continue
            if proposer.name in round_self_matches:
                continue
            # Check if this proposer is now matched or rejected
            if proposer.match is not None and isinstance(proposer.match, Responder):
                tentative_matches.append(ProposalAction(proposer=proposer.name, responder=proposer.match.name))
            elif proposer.last_proposal is not None and isinstance(proposer.last_proposal, Responder):
                # They proposed but are not matched -> rejected
                rejections.append(ProposalAction(proposer=proposer.name, responder=proposer.last_proposal.name))

        steps.append(
            RoundStep(
                round=round_num,
                proposals=proposals,
                rejections=rejections,
                tentative_matches=tentative_matches,
                self_matches=round_self_matches,
            )
        )

    # Finalize: set unmatched responders to self-match (same as Algorithm.execute)
    for responder in algorithm.responders:
        if not responder.is_matched:
            responder.match = responder

    # Build final result
    matches: dict[str, str] = {}
    unmatched: list[str] = []
    self_matches: list[str] = []

    for proposer in algorithm.proposers:
        match proposer.match:
            case None:
                unmatched.append(proposer.name)
            case m if m.name == proposer.name:
                self_matches.append(proposer.name)
            case m:
                matches[proposer.name] = m.name

    for responder in algorithm.responders:
        match responder.match:
            case m if m == responder:
                self_matches.append(responder.name)
            case None:
                unmatched.append(responder.name)

    result = MatchingResult(
        rounds=algorithm.round,
        matches=matches,
        unmatched=unmatched,
        self_matches=self_matches,
        all_matched=len(unmatched) == 0 and len(self_matches) == 0,
    )
    stability = check_stability(algorithm)

    return StepsResponse(
        steps=steps,
        final_result=_build_matching_response(result, stability),
    )

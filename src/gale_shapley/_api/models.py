"""Pydantic request/response models for the API."""

from pydantic import BaseModel


class MatchingRequest(BaseModel):
    """Request body for matching endpoints."""

    proposer_preferences: dict[str, list[str]]
    responder_preferences: dict[str, list[str]]


class ProposalAction(BaseModel):
    """A proposer-responder pair representing an action."""

    proposer: str
    responder: str


class MatchingResponse(BaseModel):
    """Response for the matching endpoint, combines MatchingResult and StabilityResult."""

    rounds: int
    matches: dict[str, str]
    unmatched: list[str]
    self_matches: list[str]
    all_matched: bool
    is_stable: bool
    is_individually_rational: bool
    blocking_pairs: list[tuple[str, str]]


class RoundStep(BaseModel):
    """Snapshot of a single round of the algorithm."""

    round: int
    proposals: list[ProposalAction]
    rejections: list[ProposalAction]
    tentative_matches: list[ProposalAction]
    self_matches: list[str]


class StepsResponse(BaseModel):
    """Response for the step-through endpoint."""

    steps: list[RoundStep]
    final_result: MatchingResponse

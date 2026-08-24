"use client";

import { useEffect, useState } from "react";
import AppShell from "@/components/layout/AppShell";
import { api } from "@/lib/api";

type Candidate = {
    _id: string;
    name?: string;
    email?: string;
};

type Job = {
    _id: string;
    title?: string;
};

type MatchResult = {
    overall_score: number;
    recommendation: string;
    scores: {
        technical_fit: number;
        responsibility_fit: number;
        domain_fit: number;
        experience_fit: number;
        education_fit: number;
    };
    matched_requirements: any[];
    eligibility_requirements?: any[];
    skill_gaps: any[];
    strengths: string[];
    gaps: string[];
    justification: string;
};

export default function MatchesPage() {
    const [candidates, setCandidates] = useState<Candidate[]>([]);
    const [jobs, setJobs] = useState<Job[]>([]);

    const [candidateSearch, setCandidateSearch] = useState("");
    const [jobSearch, setJobSearch] = useState("");

    const [candidateId, setCandidateId] = useState("");
    const [jobId, setJobId] = useState("");

    const [loadingCandidates, setLoadingCandidates] = useState(false);
    const [loadingJobs, setLoadingJobs] = useState(false);
    const [matching, setMatching] = useState(false);

    const [result, setResult] = useState<MatchResult | null>(null);
    const [error, setError] = useState("");

    const loadCandidates = async () => {
        setLoadingCandidates(true);
        setError("");

        try {
            const response = await api.get("/api/resumes", {
                params: {
                    search: candidateSearch,
                    limit: 20,
                },
            });

            setCandidates(response.data.candidates || []);
        } catch (err: any) {
            console.error("CANDIDATE LOAD ERROR:", err);
            setError(
                err.response?.data?.detail ||
                    "Failed to load candidates.",
            );
        } finally {
            setLoadingCandidates(false);
        }
    };

    const loadJobs = async () => {
        setLoadingJobs(true);
        setError("");

        try {
            const response = await api.get("/api/jobs", {
                params: {
                    search: jobSearch,
                    limit: 20,
                },
            });

            setJobs(response.data.jobs || []);
        } catch (err: any) {
            console.error("JOB LOAD ERROR:", err);
            setError(
                err.response?.data?.detail ||
                    "Failed to load jobs.",
            );
        } finally {
            setLoadingJobs(false);
        }
    };

    useEffect(() => {
        loadCandidates();
        loadJobs();
    }, []);

    const runMatch = async () => {
        if (!candidateId || !jobId) {
            setError("Please select both a candidate and a job.");
            return;
        }

        setMatching(true);
        setError("");
        setResult(null);

        try {
            const response = await api.post("/api/matches", {
                candidate_id: candidateId,
                job_id: jobId,
            });

            console.log("MATCH RESPONSE:", response.data);

            /*
             * New match response:
             *
             * {
             *   match_id: "...",
             *   candidate_id: "...",
             *   job_id: "...",
             *   match: { ... }
             * }
             *
             * Existing match response:
             *
             * {
             *   _id: "...",
             *   candidate_id: "...",
             *   job_id: "...",
             *   overall_score: ...,
             *   recommendation: ...,
             *   ...
             * }
             *
             * Support both.
             */
            const matchData =
                response.data.match ?? response.data;

            console.log("MATCH DATA:", matchData);

            setResult(matchData);
        } catch (err: any) {
            console.error("MATCH ERROR:", err);
            console.error(
                "MATCH ERROR RESPONSE:",
                err.response?.data,
            );

            setError(
                err.response?.data?.detail ||
                    "Failed to generate match.",
            );
        } finally {
            setMatching(false);
        }
    };

    return (
        <AppShell>
            <div>
                <h1 className="text-3xl font-bold text-slate-900">
                    Matches
                </h1>

                <p className="mt-2 text-slate-600">
                    Compare a candidate against a job using the AI
                    matching engine.
                </p>

                {/* Candidate and Job Selection */}
                <div className="mt-8 grid gap-6 lg:grid-cols-2">

                    {/* Candidate */}
                    <div className="rounded-xl border bg-white p-6 shadow-sm">
                        <h2 className="text-lg font-semibold text-slate-900">
                            Candidate
                        </h2>

                        <div className="mt-4 flex gap-2">
                            <input
                                value={candidateSearch}
                                onChange={(event) =>
                                    setCandidateSearch(
                                        event.target.value,
                                    )
                                }
                                placeholder="Search candidate..."
                                className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
                            />

                            <button
                                onClick={loadCandidates}
                                disabled={loadingCandidates}
                                className="rounded-lg bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-200 disabled:opacity-50"
                            >
                                {loadingCandidates
                                    ? "Searching..."
                                    : "Search"}
                            </button>
                        </div>

                        <div className="mt-4 space-y-2">
                            {candidates.map((candidate) => (
                                <button
                                    key={candidate._id}
                                    onClick={() => {
                                        setCandidateId(
                                            candidate._id,
                                        );
                                        setResult(null);
                                        setError("");
                                    }}
                                    className={`w-full rounded-lg border p-4 text-left ${
                                        candidateId ===
                                        candidate._id
                                            ? "border-slate-900 bg-slate-50"
                                            : "border-slate-200 hover:bg-slate-50"
                                    }`}
                                >
                                    <p className="font-medium text-slate-900">
                                        {candidate.name ||
                                            "Unnamed Candidate"}
                                    </p>

                                    {candidate.email && (
                                        <p className="mt-1 text-sm text-slate-500">
                                            {candidate.email}
                                        </p>
                                    )}
                                </button>
                            ))}

                            {!loadingCandidates &&
                                candidates.length === 0 && (
                                    <p className="py-6 text-center text-sm text-slate-500">
                                        No candidates found.
                                    </p>
                                )}
                        </div>
                    </div>

                    {/* Job */}
                    <div className="rounded-xl border bg-white p-6 shadow-sm">
                        <h2 className="text-lg font-semibold text-slate-900">
                            Job
                        </h2>

                        <div className="mt-4 flex gap-2">
                            <input
                                value={jobSearch}
                                onChange={(event) =>
                                    setJobSearch(
                                        event.target.value,
                                    )
                                }
                                placeholder="Search job..."
                                className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
                            />

                            <button
                                onClick={loadJobs}
                                disabled={loadingJobs}
                                className="rounded-lg bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-200 disabled:opacity-50"
                            >
                                {loadingJobs
                                    ? "Searching..."
                                    : "Search"}
                            </button>
                        </div>

                        <div className="mt-4 space-y-2">
                            {jobs.map((job) => (
                                <button
                                    key={job._id}
                                    onClick={() => {
                                        setJobId(job._id);
                                        setResult(null);
                                        setError("");
                                    }}
                                    className={`w-full rounded-lg border p-4 text-left ${
                                        jobId === job._id
                                            ? "border-slate-900 bg-slate-50"
                                            : "border-slate-200 hover:bg-slate-50"
                                    }`}
                                >
                                    <p className="font-medium text-slate-900">
                                        {job.title ||
                                            "Untitled Job"}
                                    </p>
                                </button>
                            ))}

                            {!loadingJobs &&
                                jobs.length === 0 && (
                                    <p className="py-6 text-center text-sm text-slate-500">
                                        No jobs found.
                                    </p>
                                )}
                        </div>
                    </div>
                </div>

                {/* Error */}
                {error && (
                    <div className="mt-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                        {error}
                    </div>
                )}

                {/* Run Match */}
                <div className="mt-6 flex justify-center">
                    <button
                        onClick={runMatch}
                        disabled={
                            matching ||
                            !candidateId ||
                            !jobId
                        }
                        className="rounded-lg bg-slate-900 px-8 py-3 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {matching
                            ? "Analyzing Match..."
                            : "Run Match"}
                    </button>
                </div>

                {/* Match Result */}
                {result && (
                    <div className="mt-8 space-y-6">

                        {/* Main Score */}
                        <div className="rounded-xl border bg-white p-8 shadow-sm">
                            <div className="flex items-center justify-between gap-6">
                                <div>
                                    <h2 className="text-2xl font-semibold text-slate-900">
                                        Match Result
                                    </h2>

                                    <p className="mt-2 text-lg text-slate-600">
                                        {result.recommendation}
                                    </p>
                                </div>

                                <div className="text-right">
                                    <p className="text-5xl font-bold text-slate-900">
                                        {result.overall_score}
                                    </p>

                                    <p className="text-sm text-slate-500">
                                        Overall Score
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Score Breakdown */}
                        {result.scores && (
                            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">

                                <ScoreCard
                                    label="Technical"
                                    score={
                                        result.scores
                                            .technical_fit
                                    }
                                    max={40}
                                />

                                <ScoreCard
                                    label="Responsibilities"
                                    score={
                                        result.scores
                                            .responsibility_fit
                                    }
                                    max={25}
                                />

                                <ScoreCard
                                    label="Domain"
                                    score={
                                        result.scores
                                            .domain_fit
                                    }
                                    max={15}
                                />

                                <ScoreCard
                                    label="Experience"
                                    score={
                                        result.scores
                                            .experience_fit
                                    }
                                    max={10}
                                />

                                <ScoreCard
                                    label="Education"
                                    score={
                                        result.scores
                                            .education_fit
                                    }
                                    max={10}
                                />

                            </div>
                        )}

                        {/* Justification */}
                        {result.justification && (
                            <div className="rounded-xl border bg-white p-6 shadow-sm">
                                <h2 className="text-lg font-semibold text-slate-900">
                                    Justification
                                </h2>

                                <p className="mt-3 leading-7 text-slate-600">
                                    {result.justification}
                                </p>
                            </div>
                        )}

                        {/* Matched Requirements */}
                        {result.matched_requirements?.length >
                            0 && (
                            <div className="rounded-xl border bg-white p-6 shadow-sm">
                                <h2 className="text-lg font-semibold text-slate-900">
                                    Matched Requirements
                                </h2>

                                <div className="mt-4 space-y-4">
                                    {result.matched_requirements.map(
                                        (item, index) => (
                                            <div
                                                key={index}
                                                className="rounded-lg border border-slate-200 p-4"
                                            >
                                                <div className="flex flex-wrap items-center justify-between gap-2">
                                                    <p className="font-medium text-slate-900">
                                                        {
                                                            item.job_requirement
                                                        }
                                                    </p>

                                                    <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
                                                        {
                                                            item.match_type
                                                        }
                                                    </span>
                                                </div>

                                                <p className="mt-2 text-sm text-slate-600">
                                                    {
                                                        item.explanation
                                                    }
                                                </p>

                                                {item.candidate_evidence && (
                                                    <p className="mt-2 text-sm text-slate-500">
                                                        <strong>
                                                            Evidence:
                                                        </strong>{" "}
                                                        {
                                                            item.candidate_evidence
                                                        }
                                                    </p>
                                                )}
                                            </div>
                                        ),
                                    )}
                                </div>
                            </div>
                        )}

                        {/* Skill Gaps */}
                        {result.skill_gaps?.length > 0 && (
                            <div className="rounded-xl border bg-white p-6 shadow-sm">
                                <h2 className="text-lg font-semibold text-slate-900">
                                    Skill Gaps
                                </h2>

                                <div className="mt-4 space-y-3">
                                    {result.skill_gaps.map(
                                        (gap, index) => (
                                            <div
                                                key={index}
                                                className="rounded-lg border border-slate-200 p-4"
                                            >
                                                <p className="font-medium text-slate-900">
                                                    {
                                                        gap.job_requirement
                                                    }
                                                </p>

                                                <p className="mt-1 text-sm text-slate-600">
                                                    {
                                                        gap.explanation
                                                    }
                                                </p>
                                            </div>
                                        ),
                                    )}
                                </div>
                            </div>
                        )}

                        {/* Strengths and Gaps */}
                        <div className="grid gap-6 lg:grid-cols-2">

                            {result.strengths?.length > 0 && (
                                <div className="rounded-xl border bg-white p-6 shadow-sm">
                                    <h2 className="text-lg font-semibold text-slate-900">
                                        Strengths
                                    </h2>

                                    <ul className="mt-4 space-y-2">
                                        {result.strengths.map(
                                            (
                                                strength,
                                                index,
                                            ) => (
                                                <li
                                                    key={index}
                                                    className="text-sm leading-6 text-slate-600"
                                                >
                                                    • {strength}
                                                </li>
                                            ),
                                        )}
                                    </ul>
                                </div>
                            )}

                            {result.gaps?.length > 0 && (
                                <div className="rounded-xl border bg-white p-6 shadow-sm">
                                    <h2 className="text-lg font-semibold text-slate-900">
                                        Gaps
                                    </h2>

                                    <ul className="mt-4 space-y-2">
                                        {result.gaps.map(
                                            (
                                                gap,
                                                index,
                                            ) => (
                                                <li
                                                    key={index}
                                                    className="text-sm leading-6 text-slate-600"
                                                >
                                                    • {gap}
                                                </li>
                                            ),
                                        )}
                                    </ul>
                                </div>
                            )}

                        </div>
                    </div>
                )}
            </div>
        </AppShell>
    );
}

function ScoreCard({
    label,
    score,
    max,
}: {
    label: string;
    score: number;
    max: number;
}) {
    return (
        <div className="rounded-xl border bg-white p-5 shadow-sm">
            <p className="text-sm text-slate-500">
                {label}
            </p>

            <p className="mt-2 text-2xl font-bold text-slate-900">
                {score}
                <span className="text-sm font-normal text-slate-400">
                    /{max}
                </span>
            </p>
        </div>
    );
}
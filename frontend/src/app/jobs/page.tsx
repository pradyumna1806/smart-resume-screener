"use client";

import { useState } from "react";
import AppShell from "@/components/layout/AppShell";
import { api } from "@/lib/api";

export default function JobsPage() {
    const [description, setDescription] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [job, setJob] = useState<any>(null);

    const extractJob = async () => {
        if (!description.trim()) {
            setError("Job description cannot be empty.");
            return;
        }

        setLoading(true);
        setError("");
        setJob(null);

        try {
            const response = await api.post("/api/jobs/extract", {
                description,
            });

            setJob(response.data);
        } catch (err: any) {
            console.error("JOB EXTRACTION ERROR:", err);
            console.error("RESPONSE:", err.response?.data);

            setError(
                err.response?.data?.detail ||
                    "Failed to process the job description.",
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <AppShell>
            <div>
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">
                        Jobs
                    </h1>

                    <p className="mt-2 text-slate-600">
                        Add job descriptions and extract structured
                        requirements using AI.
                    </p>
                </div>

                <div className="mt-8 max-w-4xl rounded-xl border bg-white p-8 shadow-sm">
                    <h2 className="text-lg font-semibold text-slate-900">
                        Job Description
                    </h2>

                    <p className="mt-2 text-sm text-slate-500">
                        Paste the complete job description below.
                    </p>

                    <textarea
                        value={description}
                        onChange={(event) => {
                            setDescription(event.target.value);
                            setError("");
                            setJob(null);
                        }}
                        placeholder="Paste the job description here..."
                        className="mt-6 min-h-80 w-full resize-y rounded-lg border border-slate-300 p-4 text-sm text-slate-900 outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
                    />

                    <div className="mt-4 flex justify-end">
                        <button
                            type="button"
                            onClick={extractJob}
                            disabled={loading}
                            className="rounded-lg bg-slate-900 px-6 py-3 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                        >
                            {loading
                                ? "Extracting..."
                                : "Extract Job Profile"}
                        </button>
                    </div>

                    {error && (
                        <div className="mt-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                            {error}
                        </div>
                    )}
                </div>

                {job && (
                    <div className="mt-8 max-w-4xl rounded-xl border bg-white p-8 shadow-sm">
                        <h2 className="text-lg font-semibold text-slate-900">
                            Extracted Job Profile
                        </h2>

                        <pre className="mt-4 overflow-auto rounded-lg bg-slate-950 p-4 text-sm text-white">
                            {JSON.stringify(job, null, 2)}
                        </pre>
                    </div>
                )}
            </div>
        </AppShell>
    );
}
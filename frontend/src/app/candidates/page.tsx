"use client";

import { useState } from "react";
import AppShell from "@/components/layout/AppShell";
import { api } from "@/lib/api";

export default function CandidatesPage() {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [candidate, setCandidate] = useState<any>(null);

    const extractProfile = async () => {
        if (!file) {
            return;
        }

        setLoading(true);
        setError("");
        setCandidate(null);

        try {
            const formData = new FormData();
            formData.append("file", file);

            const response = await api.post(
                "/api/resumes/extract",
                formData,
            );

            setCandidate(response.data);
        }catch (err: any) {
                console.error("UPLOAD ERROR:", err);
                console.error("RESPONSE:", err.response?.data);

                setError(
                    JSON.stringify(
                        err.response?.data || "Unknown error",
                        null,
                        2,
                    ),
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
                        Candidates
                    </h1>

                    <p className="mt-2 text-slate-600">
                        Upload resumes and extract structured candidate
                        profiles.
                    </p>
                </div>

                <div className="mt-8 max-w-3xl rounded-xl border bg-white p-8 shadow-sm">
                    <h2 className="text-lg font-semibold text-slate-900">
                        Upload Resume
                    </h2>

                    <p className="mt-2 text-sm text-slate-500">
                        Upload a candidate resume to extract their
                        information using AI.
                    </p>

                    <label className="mt-6 flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-slate-300 px-6 py-12 text-center hover:bg-slate-50">
                        <span className="text-sm font-medium text-slate-700">
                            {file
                                ? file.name
                                : "Click to select a resume"}
                        </span>

                        <span className="mt-2 text-xs text-slate-500">
                            PDF files only
                        </span>

                        <input
                            type="file"
                            className="hidden"
                            accept=".pdf"
                            onChange={(event) => {
                                const selectedFile =
                                    event.target.files?.[0] ?? null;

                                setFile(selectedFile);
                                setCandidate(null);
                                setError("");
                            }}
                        />
                    </label>

                    {file && (
                        <div className="mt-6 flex items-center justify-between rounded-lg bg-slate-50 px-4 py-3">
                            <div>
                                <p className="text-sm font-medium text-slate-900">
                                    {file.name}
                                </p>

                                <p className="text-xs text-slate-500">
                                    {(file.size / 1024).toFixed(1)} KB
                                </p>
                            </div>

                            <button
                                type="button"
                                onClick={extractProfile}
                                disabled={loading}
                                className="rounded-lg bg-slate-900 px-5 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                {loading
                                    ? "Extracting..."
                                    : "Extract Profile"}
                            </button>
                        </div>
                    )}

                    {error && (
                        <div className="mt-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                            {error}
                        </div>
                    )}
                </div>

                {candidate && (
                    <div className="mt-8 max-w-3xl rounded-xl border bg-white p-8 shadow-sm">
                        <h2 className="text-lg font-semibold text-slate-900">
                            Candidate Profile
                        </h2>

                        <p className="mt-2 text-sm text-slate-600">
                            Candidate profile successfully extracted and saved.
                        </p>
                    </div>
                )}
            </div>
        </AppShell>
    );
}
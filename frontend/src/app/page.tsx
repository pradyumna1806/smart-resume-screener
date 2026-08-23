import AppShell from "@/components/layout/AppShell";

export default function Home() {
    return (
        <AppShell>
            <div>
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">
                        Dashboard
                    </h1>

                    <p className="mt-2 text-slate-600">
                        Evaluate candidates against job requirements
                        using evidence-based AI matching.
                    </p>
                </div>

                <div className="mt-8 grid gap-6 md:grid-cols-3">
                    <DashboardCard
                        title="Candidates"
                        description="Manage uploaded resumes and candidate profiles."
                    />

                    <DashboardCard
                        title="Jobs"
                        description="Create and manage job descriptions."
                    />

                    <DashboardCard
                        title="Matches"
                        description="Review candidate-job matching results."
                    />
                </div>

                <div className="mt-8 rounded-xl border bg-white p-6 shadow-sm">
                    <h2 className="text-lg font-semibold text-slate-900">
                        Recent Matches
                    </h2>

                    <p className="mt-2 text-sm text-slate-500">
                        Matching activity will appear here once candidates
                        and jobs are processed.
                    </p>
                </div>
            </div>
        </AppShell>
    );
}

function DashboardCard({
    title,
    description,
}: {
    title: string;
    description: string;
}) {
    return (
        <div className="rounded-xl border bg-white p-6 shadow-sm">
            <h2 className="font-semibold text-slate-900">
                {title}
            </h2>

            <p className="mt-2 text-sm text-slate-500">
                {description}
            </p>
        </div>
    );
}
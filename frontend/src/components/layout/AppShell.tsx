import Sidebar from "./Sidebar";

export default function AppShell({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex min-h-screen bg-slate-50">
            <Sidebar />

            <div className="flex min-w-0 flex-1 flex-col">
                <header className="flex h-16 items-center justify-between border-b bg-white px-8">
                    <div>
                        <p className="text-sm text-slate-500">
                            Candidate evaluation platform
                        </p>
                    </div>

                    <div className="text-sm font-medium text-slate-700">
                        Recruiter
                    </div>
                </header>

                <main className="flex-1 p-8">
                    {children}
                </main>
            </div>
        </div>
    );
}